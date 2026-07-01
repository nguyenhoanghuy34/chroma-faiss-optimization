import uuid


def generate_id():
    """
    Tạo ID duy nhất.
    """

    return str(uuid.uuid4())


def clean_text(text):
    """
    Chuẩn hóa text.
    """

    if not text:
        return ""

    text = text.strip()
    text = " ".join(text.split())

    return text


def chunk_text(
    text,
    chunk_size=500,
    overlap=50
):
    """
    Chia text thành các đoạn nhỏ.

    chunk_size: số ký tự mỗi chunk
    overlap: phần trùng giữa các chunk
    """

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start = end - overlap

    return chunks