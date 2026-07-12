from config import LABOR_LAW_TXT_PATH


def load_txt():

    with open(
        LABOR_LAW_TXT_PATH,
        "r",
        encoding="utf-8"
    ) as f:
        text = f.read()

    return text