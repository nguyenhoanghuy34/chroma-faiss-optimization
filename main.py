from src.loader.pdf_loader import load_pdf
from src.loader.txt_loader import load_txt
from src.chunking.chunker import chunker

def main():

    chunks = chunker()

if __name__ == "__main__":
    main()