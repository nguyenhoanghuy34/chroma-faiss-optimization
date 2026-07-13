from src.loader.pdf_loader import load_pdf
from src.loader.txt_loader import load_txt
from src.chunking.chunker import chunker
from src.embedding.embedder import create_embedding
from src.test.test_retrieval import test_retrieval
from src.rag.pipeline import ask

def main():

    question = """
    Người sử dụng lao động có được giữ giấy tờ tùy thân
    của người lao động không?
    """

    print("=" * 80)
    print("QUESTION:")
    print(question)

    print("=" * 80)
    print("START ASK")

    answer = ask(
        question
    )

    print("=" * 80)
    print("ANSWER:")
    print(answer)


if __name__ == "__main__":
    main()











