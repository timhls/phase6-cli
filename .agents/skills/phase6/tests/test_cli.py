from unittest.mock import MagicMock, patch

from pyphase6.cli import app, strip_html
from pyphase6.models import (
    CardContent,
    CardProgress,
    Subject,
    SubjectContent,
    SubjectIdOwner,
    VocabItem,
    VocabList,
)
from typer.testing import CliRunner

runner = CliRunner()


def test_strip_html():
    assert strip_html("<p>Hello</p>") == "Hello"
    assert strip_html("<b>Bold</b> and <i>Italic</i>") == "Bold and Italic"
    assert strip_html("No HTML") == "No HTML"


@patch("pyphase6.cli.get_authenticated_client")
def test_subjects_command(mock_get_client):
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client

    # Mock return subjects
    mock_sub = MagicMock()
    mock_sub.subjectId.id = "sub123"
    mock_sub.subjectContent.name = "My Test Subject"
    mock_sub.subjectContent.primaryLang = "en"
    mock_sub.subjectContent.secondaryLang = "de"
    mock_client.get_subjects.return_value = [mock_sub]

    result = runner.invoke(app, ["subjects"])
    assert result.exit_code == 0
    assert "Your Phase-6 Subjects" in result.stdout
    assert "sub123" in result.stdout
    assert "My Test Subject" in result.stdout
    assert "en" in result.stdout
    assert "de" in result.stdout


@patch("pyphase6.cli.get_authenticated_client")
def test_add_command(mock_get_client):
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    mock_client.add_vocabulary.return_value = "new_card_uuid"

    result = runner.invoke(app, ["add", "sub123", "Front Side", "Back Side"])

    assert result.exit_code == 0
    assert "Successfully added card new_card_uuid" in result.stdout
    mock_client.add_vocabulary.assert_called_once_with(
        "sub123", "<p>Front Side</p>", "<p>Back Side</p>", unit_id=None
    )


@patch("pyphase6.cli.get_authenticated_client")
def test_add_command_with_html(mock_get_client):
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    mock_client.add_vocabulary.return_value = "new_card_uuid"

    # Passing HTML directly should prevent double wrapping
    result = runner.invoke(app, ["add", "sub123", "<p><b>Front</b> Side</p>", "<p>Back Side</p>"])

    assert result.exit_code == 0
    mock_client.add_vocabulary.assert_called_once_with(
        "sub123", "<p><b>Front</b> Side</p>", "<p>Back Side</p>", unit_id=None
    )


@patch("pyphase6.cli.get_authenticated_client")
def test_add_command_with_unit(mock_get_client):
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    mock_client.get_or_create_unit.return_value = "unit123"
    mock_client.add_vocabulary.return_value = "new_card_uuid"

    result = runner.invoke(app, ["add", "sub123", "Front Side", "Back Side", "--unit", "Unit A"])

    assert result.exit_code == 0
    assert "Looking up or creating unit 'Unit A'..." in result.stdout
    assert "Successfully added card new_card_uuid" in result.stdout
    mock_client.get_or_create_unit.assert_called_once_with("sub123", "Unit A")
    mock_client.add_vocabulary.assert_called_once_with(
        "sub123", "<p>Front Side</p>", "<p>Back Side</p>", unit_id="unit123"
    )


@patch("pyphase6.cli.get_authenticated_client")
def test_update_command(mock_get_client):
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client

    result = runner.invoke(app, ["update", "sub123", "card456", "New Question", "New Answer"])

    assert result.exit_code == 0
    assert "Successfully updated card card456" in result.stdout
    mock_client.update_vocabulary.assert_called_once_with(
        "sub123", "card456", "<p>New Question</p>", "<p>New Answer</p>", unit_id=None
    )


@patch("pyphase6.cli.get_authenticated_client")
def test_delete_command(mock_get_client):
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client

    result = runner.invoke(app, ["delete", "card456"])

    assert result.exit_code == 0
    assert "Successfully deleted card card456" in result.stdout
    mock_client.delete_vocabulary.assert_called_once_with("card456")


@patch("pyphase6.cli.get_authenticated_client")
def test_delete_unit_command(mock_get_client):
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client

    result = runner.invoke(app, ["delete-unit", "unit123"])

    assert result.exit_code == 0
    assert "Successfully deleted unit unit123" in result.stdout
    mock_client.delete_unit.assert_called_once_with("unit123")


@patch("pyphase6.cli.get_authenticated_client")
def test_subjects_command_json(mock_get_client):
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    mock_client.get_subjects.return_value = [
        Subject(
            subjectId=SubjectIdOwner(id="sub123", ownerId="owner1"),
            subjectContent=SubjectContent(name="My Test Subject", primaryLang="en"),
        )
    ]

    result = runner.invoke(app, ["subjects", "--json"])

    assert result.exit_code == 0
    assert '"sub123"' in result.stdout
    assert '"My Test Subject"' in result.stdout
    assert '"owner1"' in result.stdout
    assert "Your Phase-6 Subjects" not in result.stdout


@patch("pyphase6.cli.get_authenticated_client")
def test_vocab_command_json(mock_get_client):
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    mock_client.get_vocabulary.return_value = VocabList(
        items=[
            VocabItem(
                cardIdString="abcdef123456",
                cardContent=CardContent(question="<p>Hello</p>", answer="<p>Hallo</p>"),
                normal=CardProgress(active=True, isDue=False, phase=3),
            )
        ]
    )

    result = runner.invoke(app, ["vocab", "sub123", "--json"])

    assert result.exit_code == 0
    assert '"abcdef123456"' in result.stdout
    assert '"<p>Hello</p>"' in result.stdout
    assert "Vocabulary Items" not in result.stdout


@patch("pyphase6.cli.Phase6Client")
def test_login_command_uses_env_vars(mock_client_cls, monkeypatch):
    monkeypatch.setenv("PHASE6_USERNAME", "user@example.com")
    monkeypatch.setenv("PHASE6_PASSWORD", "secret")

    result = runner.invoke(app, ["login"])

    assert result.exit_code == 0
    mock_client_cls.return_value.login.assert_called_once_with("user@example.com", "secret")
    assert "Successfully logged in" in result.stdout


@patch("pyphase6.cli.get_authenticated_client")
def test_vocab_command(mock_get_client):
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client

    mock_item = MagicMock()
    mock_item.cardIdString = "abcdef123456"
    mock_item.cardContent.question = "<p>Hello</p>"
    mock_item.cardContent.answer = "<p>Hallo</p>"
    mock_item.normal.phase = 3

    mock_vocab_list = MagicMock()
    mock_vocab_list.items = [mock_item]
    mock_client.get_vocabulary.return_value = mock_vocab_list

    result = runner.invoke(app, ["vocab", "sub123"])

    assert result.exit_code == 0
    assert "Hello" in result.stdout
    assert "Hallo" in result.stdout
    mock_client.get_vocabulary.assert_called_once_with(subject_id="sub123", limit=100)
