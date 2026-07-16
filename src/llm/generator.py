import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM
)

from config import LLM_MODEL_NAME

_model = None
_tokenizer = None

def load_llm():
    global _model
    global _tokenizer
    if _model is None:
        print(
            "Loading LLM..."
        )
        _tokenizer = AutoTokenizer.from_pretrained(
            LLM_MODEL_NAME
        )
        _model = AutoModelForCausalLM.from_pretrained(
            LLM_MODEL_NAME,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        print(
            "LLM ready!"
        )
    return _model, _tokenizer


def generate_answer(
        prompt,
        max_tokens=512
):
    model, tokenizer = load_llm()
    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    )
    inputs = {
        k:v.to(model.device)
        for k,v in inputs.items()
    }
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_tokens,
        temperature=0.2,
        do_sample=True
    )
    answer = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return answer