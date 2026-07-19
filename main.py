from src.loader.pdf_loader import load_pdf
from src.loader.txt_loader import load_txt
from src.chunking.chunker import chunker
from src.embedding.embedder import create_embedding
from src.test.test_retrieval import test_retrieval
from src.rag.pipeline import ask
from src.routing.router_service import route


def main():

    question = input("Question: ")

    result = route(question)

    print()

    print("=" * 50)

    print(result)



if __name__ == "__main__":
    main()











