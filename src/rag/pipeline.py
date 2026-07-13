from src.retrieval.retriever import retrieve
from src.llm.generator import generate_answer



# =====================================
# Build Prompt
# =====================================

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

Nhiệm vụ:
- Trả lời câu hỏi dựa trên Bộ luật Lao động 2019.
- Chỉ sử dụng thông tin trong CONTEXT.
- Không tự suy luận hoặc thêm thông tin ngoài dữ liệu.
- Nếu CONTEXT không có câu trả lời, hãy trả lời:
"Không tìm thấy quy định phù hợp trong dữ liệu."

========================
CONTEXT
========================

{context}


========================
CÂU HỎI
========================

{question}


========================
TRẢ LỜI
========================

"""


    return prompt




# =====================================
# RAG Pipeline
# =====================================

def ask(
        question
):


    # -------------------------
    # 1. Retrieve documents
    # -------------------------

    results = retrieve(
        question
    )



    if not results:

        return "Không tìm thấy quy định phù hợp trong dữ liệu."



    # -------------------------
    # 2. Extract context
    # -------------------------

    documents = []


    for item in results:


        documents.append(
            item["content"]
        )



    # -------------------------
    # 3. Build prompt
    # -------------------------

    prompt = build_prompt(

        question,

        documents

    )



    # -------------------------
    # 4. Generate answer
    # -------------------------

    answer = generate_answer(

        prompt

    )



    return answer