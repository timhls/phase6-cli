from pyphase6.client import Phase6Client
import os

def run():
    c = Phase6Client()
    # "Chinesisch-Deutsch" subject id: 0b82cb9c-0175-490d-d14f-8c7c400a4c1f
    vocab = c.get_vocabulary("0b82cb9c-0175-490d-d14f-8c7c400a4c1f")
    print(vocab.model_dump())

if __name__ == "__main__":
    run()
