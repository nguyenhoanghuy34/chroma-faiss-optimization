from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


def get_embedding_model():

    model = SentenceTransformer(
        MODEL_NAME,
        device="cpu"
    )

    return model