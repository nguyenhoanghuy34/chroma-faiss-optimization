import chromadb

from chromadb.utils import embedding_functions

from config import (
    VECTOR_STORE_PATH,
    EMBEDDING_MODEL_NAME,
    CHROMA_COLLECTION_NAME,
    RETRIEVAL_TOP_K
)



# =====================================
# INITIALIZE CHROMA
# =====================================


client = chromadb.PersistentClient(
    path=VECTOR_STORE_PATH
)



embedding_function = (
    embedding_functions
    .SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL_NAME
    )
)



try:

    collection = client.get_collection(

        name=CHROMA_COLLECTION_NAME,

        embedding_function=embedding_function

    )


except Exception as e:

    raise Exception(
        f"Cannot load collection: {CHROMA_COLLECTION_NAME}"
    ) from e





# =====================================
# RETRIEVAL
# =====================================


def retrieve(query, top_k=RETRIEVAL_TOP_K):


    results = collection.query(

        query_texts=[
            query
        ],

        n_results=top_k

    )



    formatted_results = []



    for i in range(
        len(results["documents"][0])
    ):


        item = {

            "id":
                results["ids"][0][i],


            "content":
                results["documents"][0][i],


            "metadata":
                results["metadatas"][0][i],


            "distance":
                results["distances"][0][i]

        }


        formatted_results.append(
            item
        )



    return formatted_results