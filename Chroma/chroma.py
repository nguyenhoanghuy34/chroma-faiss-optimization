from Dataset.data_loader import load_squad


def execute_chroma(limit=10):

    docs = load_squad(limit=limit)

    for doc in docs:
        print(doc)