from src.loader.pdf_loader import load_pdf
from src.loader.txt_loader import load_txt

def main():

    text = load_txt()

    print("\nPreview:")
    print(text[:1000])


if __name__ == "__main__":
    main()