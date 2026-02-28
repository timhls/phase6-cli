import re
import csv
import json
from pathlib import Path
from rich.progress import track
import typer
from rich.console import Console
from rich.table import Table

from pyphase6.client import Phase6Client, AuthError, APIConnectionError

app = typer.Typer(help="CLI for managing Phase-6 vocabulary")
console = Console()


def get_authenticated_client() -> Phase6Client:
    client = Phase6Client()
    if not client.session_file.exists():
        console.print("[red]Not logged in. Please run 'pyphase6 login' first.[/red]")
        raise typer.Exit(1)
    return client


@app.command()
def login(
    username: str = typer.Option(..., prompt=True, help="Your Phase-6 email address"),
    password: str = typer.Option(..., prompt=True, hide_input=True, help="Your Phase-6 password"),
):
    """Authenticate with the Phase-6 platform and save the session."""
    client = Phase6Client()
    with console.status(f"Logging in as {username} (this opens a headless browser)..."):
        try:
            client.login(username, password)
            console.print("[green]Successfully logged in and saved session![/green]")
        except AuthError as e:
            console.print(f"[red]{e}[/red]")
            raise typer.Exit(1)


@app.command()
def subjects():
    """List all vocabulary subjects (books/lists) you own."""
    client = get_authenticated_client()
    with console.status("Fetching subjects using automated browser..."):
        try:
            subs = client.get_subjects()
        except APIConnectionError as e:
            console.print(f"[red]{e}[/red]")
            raise typer.Exit(1)

    table = Table(title="Your Phase-6 Subjects")
    table.add_column("Subject ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Primary Lang", style="green")
    table.add_column("Secondary Lang", style="blue")

    for s in subs:
        table.add_row(
            s.subjectId.id,
            s.subjectContent.name,
            s.subjectContent.primaryLang or "N/A",
            s.subjectContent.secondaryLang or "N/A",
        )

    console.print(table)


@app.command()
def vocab(
    subject_id: str = typer.Argument(..., help="The ID of the subject to fetch vocabulary for"),
    limit: int = typer.Option(100, help="Maximum number of items to fetch"),
):
    """List vocabulary items for a specific subject."""
    client = get_authenticated_client()
    with console.status(f"Fetching vocabulary for subject {subject_id}..."):
        try:
            vocab_list = client.get_vocabulary(subject_id=subject_id, limit=limit)
        except APIConnectionError as e:
            console.print(f"[red]{e}[/red]")
            raise typer.Exit(1)

    table = Table(title=f"Vocabulary Items (Showing {len(vocab_list.items)})")
    table.add_column("Card ID", style="cyan", no_wrap=True)
    table.add_column("Question", style="magenta")
    table.add_column("Answer", style="green")
    table.add_column("Phase", style="yellow")

    for item in vocab_list.items:
        question = strip_html(item.cardContent.question) if item.cardContent else "N/A"
        answer = strip_html(item.cardContent.answer) if item.cardContent else "N/A"

        # Clean up the weird formatting we saw in the answer JSON like: Sohn[{~hefei_huang_verlag*...~}]
        if "[" in answer and "~" in answer:
            answer = answer.split("[")[0].strip()
        if "[" in question and "~" in question:
            question = question.split("[")[0].strip()

        phase = str(item.normal.phase) if item.normal else "N/A"

        table.add_row(item.cardIdString[:8] + "...", question, answer, phase)

    console.print(table)


def strip_html(text):
    return re.sub(r"<[^>]+>", "", text)


@app.command()
def add(
    subject_id: str = typer.Argument(..., help="Subject ID to add to"),
    question: str = typer.Argument(..., help="Front of the card"),
    answer: str = typer.Argument(..., help="Back of the card"),
):
    """Add a new vocabulary card to a subject."""
    client = get_authenticated_client()
    with console.status(f"Adding card to {subject_id}..."):
        try:
            # Wrap in paragraph tags if not present, as the server expects rich text
            q_html = f"<p>{question}</p>" if not question.startswith("<p>") else question
            a_html = f"<p>{answer}</p>" if not answer.startswith("<p>") else answer
            card_id = client.add_vocabulary(subject_id, q_html, a_html)
            console.print(f"[green]Successfully added card {card_id}[/green]")
        except APIConnectionError as e:
            console.print(f"[red]{e}[/red]")
            raise typer.Exit(1)


@app.command()
def update(
    subject_id: str = typer.Argument(..., help="Subject ID the card belongs to"),
    card_id: str = typer.Argument(..., help="ID of the card to update"),
    question: str = typer.Argument(..., help="New front of the card"),
    answer: str = typer.Argument(..., help="New back of the card"),
):
    """Update an existing vocabulary card."""
    client = get_authenticated_client()
    with console.status(f"Updating card {card_id}..."):
        try:
            q_html = f"<p>{question}</p>" if not question.startswith("<p>") else question
            a_html = f"<p>{answer}</p>" if not answer.startswith("<p>") else answer
            client.update_vocabulary(subject_id, card_id, q_html, a_html)
            console.print(f"[green]Successfully updated card {card_id}[/green]")
        except APIConnectionError as e:
            console.print(f"[red]{e}[/red]")
            raise typer.Exit(1)


@app.command()
def delete(
    card_id: str = typer.Argument(..., help="ID of the card to delete"),
):
    """Delete a vocabulary card."""
    client = get_authenticated_client()
    with console.status(f"Deleting card {card_id}..."):
        try:
            client.delete_vocabulary(card_id)
            console.print(f"[green]Successfully deleted card {card_id}[/green]")
        except APIConnectionError as e:
            console.print(f"[red]{e}[/red]")
            raise typer.Exit(1)


@app.command(name="import")
def import_vocab(
    subject_id: str = typer.Argument(..., help="Subject ID to import into"),
    file_path: Path = typer.Argument(..., help="Path to CSV or JSON file"),
):
    """Bulk import vocabulary from a CSV or JSON file."""
    client = get_authenticated_client()

    if not file_path.exists():
        console.print(f"[red]File not found: {file_path}[/red]")
        raise typer.Exit(1)

    items = []

    if file_path.suffix.lower() == ".csv":
        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                q = row.get("question") or row.get("front") or row.get("q")
                a = row.get("answer") or row.get("back") or row.get("a")
                if q and a:
                    items.append((q, a))
    elif file_path.suffix.lower() == ".json":
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
            for row in data:
                if isinstance(row, dict):
                    q = row.get("question") or row.get("front") or row.get("q")
                    a = row.get("answer") or row.get("back") or row.get("a")
                    if q and a:
                        items.append((q, a))
    else:
        console.print("[red]Unsupported file format. Please use .csv or .json[/red]")
        raise typer.Exit(1)

    if not items:
        console.print(
            "[yellow]No valid items found. Ensure headers/keys are 'question' and 'answer'.[/yellow]"
        )
        raise typer.Exit(1)

    success_count = 0
    console.print(f"Found {len(items)} items to import into subject {subject_id}.")

    for q, a in track(items, description="Importing..."):
        try:
            q_html = f"<p>{q}</p>" if not q.startswith("<p>") else q
            a_html = f"<p>{a}</p>" if not a.startswith("<p>") else a
            client.add_vocabulary(subject_id, q_html, a_html)
            success_count += 1
        except APIConnectionError as e:
            console.print(f"[red]Failed to add '{q}': {e}[/red]")

    console.print(f"[green]Successfully imported {success_count}/{len(items)} cards![/green]")


if __name__ == "__main__":
    app()
