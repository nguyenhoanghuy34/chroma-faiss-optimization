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



# =====================================
# CLEAN METADATA FOR CHROMA
# =====================================

def clean_metadata(metadata):

    """
    Chroma metadata chỉ nhận:
    str | int | float | bool
    """

    result = {}


    default_keys = [
        "chapter",
        "article",
        "paragraph",
        "points",
        "level"
    ]


    # đảm bảo luôn đủ field

    for key in default_keys:

        value = metadata.get(
            key,
            ""
        )


        if isinstance(value, list):

            value = " | ".join(value)


        elif isinstance(value, dict):

            value = str(value)


        elif value is None:

            value = ""


        result[key] = str(value)



    return result




# =====================================
# CREATE EMBEDDING
# =====================================

def create_embedding():


    print(
        "Loading chunks..."
    )



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



    # ===============================
    # Chroma client
    # ===============================


    client = chromadb.PersistentClient(
        path=VECTOR_STORE_PATH
    )



    # ===============================
    # Embedding model
    # ===============================


    embedding_function = (
        embedding_functions
        .SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL_NAME
        )
    )



    # ===============================
    # Remove old collection
    # ===============================


    try:

        client.delete_collection(
            name=CHROMA_COLLECTION_NAME
        )

        print(
            "Deleted old collection"
        )


    except Exception:

        pass




    collection = client.create_collection(

        name=CHROMA_COLLECTION_NAME,

        embedding_function=embedding_function

    )



    ids = []

    documents = []

    metadatas = []



    # ===============================
    # Prepare data
    # ===============================


    for item in chunks:


        ids.append(
            item["id"]
        )


        documents.append(
            item["content"]
        )


        metadatas.append(

            clean_metadata(
                item.get(
                    "metadata",
                    {}
                )
            )

        )



    print(
        "Embedding and saving..."
    )



    # ===============================
    # Add to Chroma
    # ===============================


    collection.add(

        ids=ids,

        documents=documents,

        metadatas=metadatas

    )



    print(
        "Embedding completed!"
    )


    print(
        f"Saved vector store: {VECTOR_STORE_PATH}"
    )



    print(
        f"Collection: {CHROMA_COLLECTION_NAME}"
    )



    return collection