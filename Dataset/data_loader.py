from datasets import load_dataset


def load_squad(split="train", limit=None):
    dataset = load_dataset(
        "rajpurkar/squad",
        split=split
    )

    documents = []

    for item in dataset:
        documents.append({
            "text": item["context"],
            "question": item["question"],
            "answer": item["answers"]["text"]
        })

        if limit and len(documents) >= limit:
            break

    return documents