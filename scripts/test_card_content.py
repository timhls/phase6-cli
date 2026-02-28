from pathlib import Path
from pyphase6.client import Phase6Client


def run():
    c = Phase6Client()
    # "Chinesisch-Deutsch" subject id: 0b82cb9c-0175-490d-d14f-8c7c400a4c1f
    vocab_data = None
    with (
        c._sync_playwright()
        if hasattr(c, "_sync_playwright")
        else open(Path("~/.config/pyphase6/session.json").expanduser()) as f
    ):
        pass  # we just want the raw data!


if __name__ == "__main__":
    pass
