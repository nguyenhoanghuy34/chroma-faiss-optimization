from Dataset.data_loader import load_squad

def execute(limit=10):
    docs = load_squad(limit=limit)

    for doc in docs:
        print(doc)

    return docs