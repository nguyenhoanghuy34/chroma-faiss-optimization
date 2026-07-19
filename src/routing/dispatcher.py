from pathlib import Path

from src.llm.generator import generate_answer
from src.rag.pipeline import rag_pipeline
from src.routing.routes import GENERAL, LABOR_LAW


PROMPT_PATH = (
    Path(__file__).resolve().parent.parent
    / "prompts"
    / "chat.txt"
)


def load_chat_prompt():
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()


def dispatch(route: str, question: str):

    if route == GENERAL:

        prompt = load_chat_prompt()
        prompt = prompt.replace("{question}", question)

        return generate_answer(prompt)

    if route == LABOR_LAW:
        return rag_pipeline(question)

    raise ValueError(f"Unknown route: {route}")