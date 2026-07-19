from src.loader.pdf_loader import load_pdf
from src.loader.txt_loader import load_txt
from src.chunking.chunker import chunker
from src.embedding.embedder import create_embedding
from src.test.test_retrieval import test_retrieval
from src.routing.router_service import route
from src.routing.dispatcher import dispatch

def main():
    question = input("Question: ")
    route_name = route(question)
    answer = dispatch(
        route_name,
        question
    )
    print(answer)

if __name__ == "__main__":
    main()











