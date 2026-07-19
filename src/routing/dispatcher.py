from llm.generator import generate_answer
from rag.pipeline import rag_pipeline

from routing.routes import (
    GENERAL,
    LABOR_LAW
)


def dispatch(route: str, question: str):

    if route == GENERAL:
        return generate_answer(question)

    if route == LABOR_LAW:
        return rag_pipeline(question)

    raise ValueError(
        f"Unknown route: {route}"
    )