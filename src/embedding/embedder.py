import json
import os
import chromadb
from chromadb.utils import embedding_functions

from config import (
    LABOR_LAW_CHUNKS_JSON_PATH,
    VECTOR_STORE_PATH,
    EMBEDDING_MODEL_NAME,
    CHROMA_COLLECTION_NAME
)


def clean_metadata(metadata):
    """
    Chroma chỉ nhận metadata dạng:
    str, int, float, bool

    Không nhận:
    list, dict
    """

    clean = {}

    if not metadata:
        return clean


    for key, value in metadata.items():

        if isinstance(value, list):

            clean[key] = " | ".join(value)


        elif isinstance(value, dict):

            clean[key] = str(value)


        else:

            clean[key] = value


    return clean



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


    # tạo folder vector store

    os.makedirs(
        VECTOR_STORE_PATH,
        exist_ok=True
    )



    # Chroma persistent database

    client = chromadb.PersistentClient(
        path=VECTOR_STORE_PATH
    )



    # Embedding model

    embedding_model = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL_NAME
    )



    # Xóa collection cũ nếu build lại

    try:

        client.delete_collection(
            CHROMA_COLLECTION_NAME
        )

        print(
            "Old collection deleted"
        )

    except Exception:

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
            clean_metadata(
                item.get("metadata", {})
            )
        )



    print(
        "Embedding and saving..."
    )


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