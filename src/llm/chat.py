from src.llm.generator import load_llm


def generate_answer(
    prompt: str,
    max_tokens: int = 512
):

    model, tokenizer = load_llm()

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        text,
        return_tensors="pt"
    )

    inputs = {
        k: v.to(model.device)
        for k, v in inputs.items()
    }

    outputs = model.generate(
        **inputs,
        max_new_tokens=max_tokens,
        temperature=0.7,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )

    generated_ids = outputs[0][inputs["input_ids"].shape[1]:]

    answer = tokenizer.decode(
        generated_ids,
        skip_special_tokens=True
    ).strip()

    return answer