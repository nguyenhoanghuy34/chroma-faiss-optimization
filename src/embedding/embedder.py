import json
import chromadb

from chromadb.utils import embedding_functions

from config import (
    LABOR_LAW_CHUNKS_JSON_PATH,
    VECTOR_STORE_PATH,
    EMBEDDING_MODEL_NAME,
    CHROMA_COLLECTION_NAME
)



def create_embedding():

    print("Loading chunks...")


    with open(
        LABOR_LAW_CHUNKS_JSON_PATH,
        "r",
        encoding="utf-8"
    ) as f:
        chunks = json.load(f)



    print(
        f"Total chunks: {len(chunks)}"
    )


    # Chroma persistent database

    client = chromadb.PersistentClient(
        path=VECTOR_STORE_PATH
    )


    # Embedding function

    embedding_model = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL_NAME
    )


    # Xóa collection cũ nếu build lại

    try:
        client.delete_collection(
            CHROMA_COLLECTION_NAME
        )

    except:
        pass



    collection = client.create_collection(
        name=CHROMA_COLLECTION_NAME,
        embedding_function=embedding_model
    )


    ids = []
    documents = []
    metadatas = []


    for item in chunks:

        ids.append(
            item["id"]
        )

        documents.append(
            item["content"]
        )

        metadatas.append(
            item["metadata"]
        )



    print("Embedding and saving...")


    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )


    print(
        "Embedding completed!"
    )


    print(
        f"Saved at: {VECTOR_STORE_PATH}"
    )