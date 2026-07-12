import os

from config import LABOR_LAW_TXT_PATH
from src.preprocessing.cleaner import clean_text


def load_txt():

    print("Đang đọc:", LABOR_LAW_TXT_PATH)


    # đọc txt gốc
    with open(
        LABOR_LAW_TXT_PATH,
        "r",
        encoding="utf-8"
    ) as f:
        text = f.read()


    # clean
    clean_result = clean_text(text)


    # lưu file sau khi clean
    clean_path = os.path.join(
        os.path.dirname(LABOR_LAW_TXT_PATH),
        "labor_law_clean.txt"
    )


    with open(
        clean_path,
        "w",
        encoding="utf-8"
    ) as f:
        f.write(clean_result)


    print("Đã lưu:", clean_path)


    return clean_result