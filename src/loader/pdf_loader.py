import os
import fitz
from config import LABOR_LAW_PDF_PATH


def load_pdf():

    print("Đang đọc:", LABOR_LAW_PDF_PATH)

    doc = fitz.open(LABOR_LAW_PDF_PATH)

    text = ""

    for page_number, page in enumerate(doc):

        print(f"Đọc trang {page_number + 1}/{len(doc)}")

        page_text = page.get_text()

        text += page_text + "\n"


    output_path = os.path.join(
        "Dataset",
        "labor_law",
        "labor_law.txt"
    )


    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:
        f.write(text)


    print("Đã lưu:", output_path)


if __name__ == "__main__":
    load_pdf()