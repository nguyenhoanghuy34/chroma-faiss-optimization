from src.loader.pdf_loader import load_pdf
from src.loader.txt_loader import load_txt
from src.chunking.chunker import chunker
from src.embedding.embedder import create_embedding
from src.test.test_retrieval import test_retrieval

def main():

    test_retrieval()

if __name__ == "__main__":
    main()











