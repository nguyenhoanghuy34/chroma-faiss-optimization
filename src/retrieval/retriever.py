import chromadb

from chromadb.utils import embedding_functions

from config import (
    VECTOR_STORE_PATH,
    EMBEDDING_MODEL_NAME,
    CHROMA_COLLECTION_NAME,
    RETRIEVAL_TOP_K
)



def retrieve(query):


    client = chromadb.PersistentClient(
        path=VECTOR_STORE_PATH
    )


    embedding_model = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL_NAME
    )


    collection = client.get_collection(
        name=CHROMA_COLLECTION_NAME,
        embedding_function=embedding_model
    )


    results = collection.query(
        query_texts=[
            query
        ],
        n_results=RETRIEVAL_TOP_K
    )


    return results