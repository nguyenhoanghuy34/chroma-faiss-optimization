# Link data pdf
import os

BASE_DIR = os.getcwd()

LABOR_LAW_PDF_PATH = os.path.join(
    BASE_DIR,
    "Dataset",
    "labor_law",
    "labor_law.pdf"
)

LABOR_LAW_TXT_PATH = os.path.join(
    BASE_DIR,
    "Dataset",
    "labor_law",
    "labor_law.txt"
)

# Text đã làm sạch
LABOR_LAW_CLEAN_TXT_PATH = os.path.join(
    BASE_DIR,
    "Dataset",
    "labor_law",
    "labor_law_clean.txt"
)

# JSON chunks đã xử lý
LABOR_LAW_CHUNKS_JSON_PATH = os.path.join(
    BASE_DIR,
    "Dataset",
    "data",
    "processed",
    "labor_law_chunks.json"
)


# ==========================
# Embedding Model
# ==========================

EMBEDDING_MODEL_NAME = "BAAI/bge-m3"


# ==========================
# Retrieval Config
# ==========================

RETRIEVAL_TOP_K = 5