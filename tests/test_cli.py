from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from pyphase6.cli import app, strip_html

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
        "sub123", "<p>Front Side</p>", "<p>Back Side</p>"
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
        "sub123", "<p><b>Front</b> Side</p>", "<p>Back Side</p>"
    )
