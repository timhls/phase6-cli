import json
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from pyphase6.client import Phase6Client, AuthError


@pytest.fixture
def mock_session_data():
    return {
        "origins": [
            {
                "origin": "https://lernen.phase-6.de",
                "localStorage": [
                    {
                        "name": "persist:user",
                        "value": json.dumps(
                            {
                                "user": json.dumps(
                                    {
                                        "jossoSessionId": "test_jauth",
                                        "email": "test@example.com",
                                        "userDnsId": "test_owner",
                                    }
                                )
                            }
                        ),
                    }
                ],
            }
        ]
    }


def test_get_api_headers_no_file():
    client = Phase6Client()
    client.session_file = Path("/nonexistent/session.json")
    with pytest.raises(AuthError, match="Not logged in"):
        client._get_api_headers()


@patch("pyphase6.client.Path.exists")
@patch("builtins.open")
def test_get_api_headers_success(mock_open, mock_exists, mock_session_data):
    mock_exists.return_value = True
    # Setup mock file read
    mock_file = MagicMock()
    mock_file.read.return_value = json.dumps(mock_session_data)
    mock_file.__enter__.return_value = mock_file
    mock_open.return_value = mock_file

    client = Phase6Client()
    headers, owner_id = client._get_api_headers()

    assert headers["x-lbtoken"] == "test@example.com"
    assert headers["x-jauthtoken"] == "test_jauth"
    assert "x-clientid" in headers
    assert owner_id == "test_owner"


@patch("pyphase6.client.Phase6Client._get_api_headers")
@patch("pyphase6.client.sync_playwright")
def test_get_subjects_success(mock_sync_playwright, mock_headers):
    mock_headers.return_value = ({"dummy": "header"}, "owner1")

    # Deep mock playwright objects
    mock_ctx = MagicMock()
    mock_p = MagicMock()
    mock_p.request.new_context.return_value = mock_ctx
    mock_sync_playwright.return_value.__enter__.return_value = mock_p

    # Mock the response
    mock_resp = MagicMock()
    mock_resp.ok = True
    mock_resp.json.return_value = {
        "httpCode": 200,
        "replyContent": {
            "subjects": [
                {
                    "subjectId": {"id": "sub1", "ownerId": "owner1"},
                    "subjectContent": {"name": "Test Subject"},
                }
            ]
        },
    }
    mock_ctx.post.return_value = mock_resp

    client = Phase6Client()
    subjects = client.get_subjects()

    assert len(subjects) == 1
    assert subjects[0].subjectId.id == "sub1"
    assert subjects[0].subjectContent.name == "Test Subject"
    mock_ctx.post.assert_called_once_with("/server.integration/subjectsCombined", data={})


@patch("pyphase6.client.Phase6Client._get_api_headers")
@patch("pyphase6.client.sync_playwright")
def test_add_vocabulary_success(mock_sync_playwright, mock_headers):
    mock_headers.return_value = ({"dummy": "header"}, "owner1")

    mock_ctx = MagicMock()
    mock_p = MagicMock()
    mock_p.request.new_context.return_value = mock_ctx
    mock_sync_playwright.return_value.__enter__.return_value = mock_p

    mock_resp = MagicMock()
    mock_resp.ok = True
    mock_resp.json.return_value = {"httpCode": 200, "replyContent": "Card saved"}
    mock_ctx.post.return_value = mock_resp

    client = Phase6Client()
    card_id = client.add_vocabulary("sub1", "<p>Q</p>", "<p>A</p>")

    assert card_id is not None
    assert isinstance(card_id, str)

    # Verify post was called
    args, kwargs = mock_ctx.post.call_args
    assert args[0].startswith("/server.integration/owner1/cards/")
    assert kwargs["data"]["question"] == "<p>Q</p>"
    assert kwargs["data"]["answer"] == "<p>A</p>"
    assert kwargs["data"]["subjectIdToOwner"]["id"] == "sub1"
