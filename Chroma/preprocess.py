from tqdm import tqdm

from Dataset.data_loader import load_squad


def clean_text(text: str) -> str:
    """
    Chuẩn hóa văn bản.
    """

    text = text.strip()
    text = " ".join(text.split())

    return text


def preprocess_squad():
    """
    Load và tiền xử lý toàn bộ SQuAD.
    """

    print("Loading SQuAD dataset...")

    raw_docs = load_squad()

    print(f"Raw documents: {len(raw_docs)}")

    processed_docs = []
    seen = set()

    whitespace_count = 0
    empty_count = 0
    duplicate_count = 0

    for idx, item in enumerate(
        tqdm(raw_docs, desc="Preprocessing", unit="doc")
    ):

        original_text = item["text"]
        text = clean_text(original_text)

        # Đếm document có thay đổi khoảng trắng
        if original_text != text:
            whitespace_count += 1

        # Bỏ document rỗng
        if not text:
            empty_count += 1
            continue

        # Bỏ document trùng
        if text in seen:
            duplicate_count += 1
            continue

        seen.add(text)

        processed_docs.append(
            {
                "id": str(idx),
                "text": text,
                "question": item["question"],
                "answer": item["answer"],
            }
        )

    print(f"Raw documents: {len(raw_docs)}")
    print(f"Documents có thay đổi khoảng trắng: {whitespace_count}")
    print(f"Documents rỗng: {empty_count}")
    print(f"Documents trùng: {duplicate_count}")
    print(f"Processed documents: {len(processed_docs)}")

    return processed_docs