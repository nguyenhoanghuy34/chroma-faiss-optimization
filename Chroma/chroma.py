from Chroma.preprocess import preprocess_squad
from Chroma.embedding import get_embedding_model
from Chroma.database import (
    create_collection,
    insert_documents,
    query_documents,
)


def execute_chroma():

    print("Connecting to Chroma...")

    collection = create_collection()

    print(f"Documents in database: {collection.count()}")

    print("Loading embedding model...")
    model = get_embedding_model()

    # Chỉ build database khi chưa có dữ liệu
    if collection.count() == 0:

        print("Database is empty.")
        print("Loading dataset...")

        docs = preprocess_squad()

        print(f"Loaded {len(docs)} documents.")

        print("Building vector database...")

        insert_documents(
            collection=collection,
            embedding_model=model,
            documents=docs,
        )

        print("Database created successfully.")

    else:

        print("Existing database found. Skip indexing.")

    print("\nReady!\n")

    while True:

        question = input("Question (type 'exit' to quit): ").strip()

        if question.lower() == "exit":
            break

        results = query_documents(
            collection=collection,
            embedding_model=model,
            question=question,
            top_k=5,
        )

        print("\nTop Results:\n")

        for i, text in enumerate(results, start=1):

            print(f"[{i}]")
            print(text)
            print("-" * 80)