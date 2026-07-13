from src.retrieval.retriever import retrieve
from src.llm.generator import generate_answer



# ==========================
# Build prompt
# ==========================


def build_prompt(
        question,
        documents
):


    context = ""


    for i, doc in enumerate(documents):

        context += f"""
[Điều luật {i+1}]

{doc}

"""


    prompt = f"""
Bạn là trợ lý pháp luật Việt Nam.

Nhiệm vụ của bạn là trả lời câu hỏi dựa trên Bộ luật Lao động 2019.

Chỉ sử dụng thông tin trong phần CONTEXT.
Không tự suy đoán.
Nếu không có thông tin, hãy trả lời:
"Không tìm thấy quy định phù hợp trong dữ liệu."

====================
CONTEXT:
====================

{context}


====================
CÂU HỎI:
====================

{question}


====================
TRẢ LỜI:
====================

"""


    return prompt





# ==========================
# RAG pipeline
# ==========================


def ask(
        question
):


    # 1. Retrieval

    results = retrieve(
        question
    )



    documents = results["documents"][0]



    # 2. Build prompt

    prompt = build_prompt(

        question,

        documents

    )



    # 3. Generate answer

    answer = generate_answer(

        prompt

    )



    return answer