import os

from transformers import GenerationConfig

from llm.generator import load_llm

BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

PROMPT_PATH = os.path.join(
    BASE_DIR,
    "prompts",
    "router.txt"
)


def load_prompt():

    with open(
        PROMPT_PATH,
        "r",
        encoding="utf-8"
    ) as f:
        return f.read()


def route_question(question):

    model, tokenizer = load_llm()

    prompt = load_prompt()

    prompt = (
        prompt +
        f"\n\nCâu hỏi:\n{question}\n\nKết quả:"
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    ).to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=5,
        temperature=0,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id
    )

    text = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    result = text[len(prompt):].strip().lower()

    if "labor_law" in result:
        return "labor_law"

    return "general"