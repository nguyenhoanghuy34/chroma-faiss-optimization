from config import LABOR_LAW_PDF_PATH
from pypdf import PdfReader
import os


def load_pdf():
    print(LABOR_LAW_PDF_PATH)

    reader = PdfReader(LABOR_LAW_PDF_PATH)

    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    output_path = os.path.join(
        "Dataset",
        "labor_law",
        "labor_law.txt"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(text)

    print("Đã lưu:", output_path)


if __name__ == "__main__":
    load_pdf()