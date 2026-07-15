from src.loader.pdf_loader import load_pdf
from src.loader.txt_loader import load_txt
from src.chunking.chunker import chunker
from src.embedding.embedder import create_embedding
from src.test.test_retrieval import test_retrieval
from src.rag.pipeline import ask

def main():

    question = """
    Một công ty yêu cầu người lao động nộp bản gốc căn cước công dân (CCCD) để giữ trong suốt thời gian làm việc nhằm đảm bảo người lao động không tự ý nghỉ việc. Theo quy định của pháp luật lao động Việt Nam, việc làm này có hợp pháp không? Nếu không, người sử dụng lao động có thể bị xử lý như thế nào?
    """

    print("=" * 80)
    print("QUESTION:")
    print(question)

    print("=" * 80)
    print("START ASK")

    answer = ask(
        question
    )

    print("=" * 80)
    print("ANSWER:")
    print(answer)


if __name__ == "__main__":
    main()











