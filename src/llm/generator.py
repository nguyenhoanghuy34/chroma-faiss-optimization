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

        print("Loading LLM...")

        _tokenizer = AutoTokenizer.from_pretrained(
            LLM_MODEL_NAME
        )

        _model = AutoModelForCausalLM.from_pretrained(
            LLM_MODEL_NAME,
            dtype=torch.float16,
            device_map="auto"
        )

        print("LLM ready!")

    return _model, _tokenizer