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


@patch("pyphase6.client.Phase6Client._get_api_headers")
@patch("pyphase6.client.sync_playwright")
def test_get_vocabulary_success(mock_sync_playwright, mock_headers):
    mock_headers.return_value = ({"dummy": "header"}, "owner1")

    mock_ctx = MagicMock()
    mock_p = MagicMock()
    mock_p.request.new_context.return_value = mock_ctx
    mock_sync_playwright.return_value.__enter__.return_value = mock_p

    mock_resp = MagicMock()
    mock_resp.ok = True
    mock_resp.json.return_value = {
        "httpCode": 200,
        "replyContent": {
            "cards": [
                {
                    "cardIdString": "card1",
                    "normal": {"active": True, "isDue": False, "phase": 2},
                    "cardContent": {"question": "Q1", "answer": "A1"},
                },
                {
                    "cardIdString": "card2",
                    "normal": {"active": True, "isDue": False, "phase": 3},
                    "cardContent": {"question": "Q2", "answer": "A2"},
                },
                {
                    "cardIdString": "card3",
                    "normal": {"active": True, "isDue": False, "phase": 4},
                    "cardContent": {"question": "Q3", "answer": "A3"},
                },
            ]
        },
    }
    mock_ctx.post.return_value = mock_resp

    client = Phase6Client()
    vocab_list = client.get_vocabulary("sub1", limit=2)

    assert len(vocab_list.items) == 2
    assert vocab_list.items[0].cardIdString == "card1"
    assert vocab_list.items[1].cardIdString == "card2"
    mock_ctx.post.assert_called_once_with(
        "/server.integration/cardList", data={"subjectId": "sub1"}
    )


@patch("pyphase6.client.Phase6Client._get_api_headers")
@patch("pyphase6.client.sync_playwright")
def test_get_vocabulary_with_offset(mock_sync_playwright, mock_headers):
    mock_headers.return_value = ({"dummy": "header"}, "owner1")

    mock_ctx = MagicMock()
    mock_p = MagicMock()
    mock_p.request.new_context.return_value = mock_ctx
    mock_sync_playwright.return_value.__enter__.return_value = mock_p

    mock_resp = MagicMock()
    mock_resp.ok = True
    mock_resp.json.return_value = {
        "httpCode": 200,
        "replyContent": {
            "cards": [
                {
                    "cardIdString": "card1",
                    "normal": {"active": True, "isDue": False, "phase": 1},
                    "cardContent": {"question": "Q1", "answer": "A1"},
                },
                {
                    "cardIdString": "card2",
                    "normal": {"active": True, "isDue": False, "phase": 2},
                    "cardContent": {"question": "Q2", "answer": "A2"},
                },
                {
                    "cardIdString": "card3",
                    "normal": {"active": True, "isDue": False, "phase": 3},
                    "cardContent": {"question": "Q3", "answer": "A3"},
                },
            ]
        },
    }
    mock_ctx.post.return_value = mock_resp

    client = Phase6Client()
    vocab_list = client.get_vocabulary("sub1", offset=1, limit=2)

    assert len(vocab_list.items) == 2
    assert vocab_list.items[0].cardIdString == "card2"
    assert vocab_list.items[1].cardIdString == "card3"


@patch("pyphase6.client.Phase6Client._get_api_headers")
@patch("pyphase6.client.sync_playwright")
def test_update_vocabulary_success(mock_sync_playwright, mock_headers):
    mock_headers.return_value = ({"dummy": "header"}, "owner1")

    mock_ctx = MagicMock()
    mock_p = MagicMock()
    mock_p.request.new_context.return_value = mock_ctx
    mock_sync_playwright.return_value.__enter__.return_value = mock_p

    mock_resp = MagicMock()
    mock_resp.ok = True
    mock_resp.json.return_value = {"httpCode": 200, "replyContent": "Card updated"}
    mock_ctx.put.return_value = mock_resp

    client = Phase6Client()
    result = client.update_vocabulary("sub1", "card123", "<p>New Q</p>", "<p>New A</p>")

    assert result is True
    args, kwargs = mock_ctx.put.call_args
    assert args[0] == "/server.integration/owner1/cards/card123"
    assert kwargs["data"]["question"] == "<p>New Q</p>"
    assert kwargs["data"]["answer"] == "<p>New A</p>"


@patch("pyphase6.client.Phase6Client._get_api_headers")
@patch("pyphase6.client.sync_playwright")
def test_delete_vocabulary_success(mock_sync_playwright, mock_headers):
    mock_headers.return_value = ({"dummy": "header"}, "owner1")

    mock_ctx = MagicMock()
    mock_p = MagicMock()
    mock_p.request.new_context.return_value = mock_ctx
    mock_sync_playwright.return_value.__enter__.return_value = mock_p

    mock_resp = MagicMock()
    mock_resp.ok = True
    mock_resp.json.return_value = {"httpCode": 200, "replyContent": "Card deleted"}
    mock_ctx.delete.return_value = mock_resp

    client = Phase6Client()
    result = client.delete_vocabulary("card123")

    assert result is True
    mock_ctx.delete.assert_called_once_with("/server.integration/owner1/cards/card123")
