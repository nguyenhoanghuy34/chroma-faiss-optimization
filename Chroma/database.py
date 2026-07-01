import chromadb

from tqdm import tqdm


DB_PATH = "Chroma/chroma_db"
COLLECTION_NAME = "squad"


def create_collection():
    """
    Tạo hoặc lấy collection Chroma.
    """

    client = chromadb.PersistentClient(path=DB_PATH)

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    return collection


def insert_documents(
    collection,
    embedding_model,
    documents,
    batch_size=500
):
    """
    Sinh embedding và lưu toàn bộ document vào Chroma.
    """

    if collection.count() > 0:
        print("Collection already exists.")
        return

    print("Preparing documents...")

    ids = [doc["id"] for doc in documents]

    texts = [doc["text"] for doc in documents]

    metadatas = [
        {
            "question": doc["question"],
            "answer": " | ".join(doc["answer"])
        }
        for doc in documents
    ]

    print("Generating embeddings...")

    embeddings = embedding_model.encode(
        texts,
        batch_size=64,
        show_progress_bar=True
    ).tolist()

    print("Saving to Chroma...")

    for i in tqdm(
        range(0, len(texts), batch_size),
        desc="Insert",
        unit="batch"
    ):

        collection.add(
            ids=ids[i:i + batch_size],
            documents=texts[i:i + batch_size],
            embeddings=embeddings[i:i + batch_size],
            metadatas=metadatas[i:i + batch_size]
        )

    print(f"Inserted {len(texts)} documents.")


def query_documents(
    collection,
    embedding_model,
    question,
    top_k=5
):
    """
    Truy vấn Chroma.
    """

    query_embedding = embedding_model.encode(
        question
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results["documents"][0]