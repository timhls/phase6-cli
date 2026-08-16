from pyphase6.models import Subject, VocabItem, VocabList


def test_subject_model():
    data = {
        "subjectId": {"id": "123", "ownerId": "owner1"},
        "subjectContent": {"name": "English Test", "primaryLang": "de", "secondaryLang": "en"},
    }

    subject = Subject(**data)
    assert subject.subjectId.id == "123"
    assert subject.subjectId.ownerId == "owner1"
    assert subject.subjectContent.name == "English Test"
    assert subject.subjectContent.primaryLang == "de"
    assert subject.subjectContent.secondaryLang == "en"
    assert subject.subjectContent.description is None


def test_vocab_item_model():
    data = {
        "cardIdString": "card123",
        "normal": {"active": True, "isDue": False, "phase": 2},
        "cardContent": {
            "question": "<p>Hello</p>",
            "answer": "<p>Hallo</p>",
            "subjectIdToOwner": {"id": "123", "ownerId": "owner1"},
        },
    }

    item = VocabItem(**data)
    assert item.cardIdString == "card123"
    assert item.normal is not None
    assert item.normal.active is True
    assert item.normal.phase == 2
    assert item.cardContent is not None
    assert item.cardContent.question == "<p>Hello</p>"
    assert item.cardContent.answer == "<p>Hallo</p>"
    assert item.cardContent.subjectIdToOwner == {"id": "123", "ownerId": "owner1"}


def test_vocab_list_model():
    data = {
        "items": [
            {
                "cardIdString": "card1",
                "normal": {"active": True, "isDue": True, "phase": 1},
                "cardContent": {"question": "Q1", "answer": "A1"},
            },
            {
                "cardIdString": "card2",
                "normal": {"active": False, "isDue": False, "phase": 6},
                "cardContent": {"question": "Q2", "answer": "A2"},
            },
        ]
    }

    vlist = VocabList(**data)
    assert len(vlist.items) == 2
    assert vlist.items[0].cardIdString == "card1"
    assert vlist.items[1].normal is not None
    assert vlist.items[1].normal.phase == 6
