import typer
from pyphase6.client import Phase6Client, AuthError

app = typer.Typer(help="CLI for managing Phase-6 vocabulary")


@app.command()
def login(
    username: str = typer.Option(..., prompt=True),
    password: str = typer.Option(..., prompt=True, hide_input=True),
):
    """Authenticate with the Phase-6 platform."""
    client = Phase6Client()
    typer.echo(f"Logging in as {username}...")
    try:
        client.login(username, password)
        typer.secho(
            "Successfully logged in! (Session cookies saved in memory for now)",
            fg=typer.colors.GREEN,
        )
        # TODO: Save session to disk (e.g. ~/.config/pyphase6/session.json)
    except AuthError as e:
        typer.secho(str(e), fg=typer.colors.RED, err=True)


@app.command()
def list():
    """List current vocabulary items."""
    typer.echo("Listing vocabulary... (Not yet implemented)")


if __name__ == "__main__":
    app()
