import torch

def generate_stepwise(
    model,
    tokenizer,
    prompt,
    max_new_tokens=10,
    top_k=5
):
    input_ids = tokenizer(prompt, return_tensors="pt")["input_ids"]
    prompt_length = input_ids.shape[1]
    
    # Store prompt tokens
    prompt_tokens = tokenizer.convert_ids_to_tokens(input_ids[0].tolist())
    
    generated_tokens = []

    for step in range(max_new_tokens):
        with torch.no_grad():
            outputs = model(input_ids)
            logits = outputs.logits

        next_token_logits = logits[0, -1]
        probs = torch.softmax(next_token_logits, dim=-1)

        top_probs, top_indices = torch.topk(probs, top_k)
        top_tokens = tokenizer.convert_ids_to_tokens(top_indices.tolist())

        next_token_id = torch.argmax(probs)
        next_token = tokenizer.convert_ids_to_tokens([next_token_id.item()])[0]

        generated_tokens.append({
            "token": next_token,
            "top_k": [
                {"token": tok, "prob": prob.item()} 
                for tok, prob in zip(top_tokens, top_probs)
            ]
        })

        input_ids = torch.cat(
            [input_ids, next_token_id.view(1, 1)],
            dim=-1
        )

    return {
        "prompt_tokens": prompt_tokens,
        "generated_tokens": generated_tokens,
        "full_text": tokenizer.decode(input_ids[0])
    }


def generate_stepwise_stream(
    model,
    tokenizer,
    prompt,
    max_new_tokens=10,
    top_k=5
):
    """
    Generator function that yields tokens one at a time for streaming
    """
    input_ids = tokenizer(prompt, return_tensors="pt")["input_ids"]
    
    # First yield prompt tokens
    prompt_tokens = tokenizer.convert_ids_to_tokens(input_ids[0].tolist())
    yield {
        "prompt_tokens": prompt_tokens,
        "token": None,
        "top_k": []
    }

    # Generate tokens one by one
    for step in range(max_new_tokens):
        with torch.no_grad():
            outputs = model(input_ids)
            logits = outputs.logits

        next_token_logits = logits[0, -1]
        probs = torch.softmax(next_token_logits, dim=-1)

        top_probs, top_indices = torch.topk(probs, top_k)
        top_tokens = tokenizer.convert_ids_to_tokens(top_indices.tolist())

        next_token_id = torch.argmax(probs)
        next_token = tokenizer.convert_ids_to_tokens([next_token_id.item()])[0]

        # Yield this token immediately
        yield {
            "prompt_tokens": None,
            "token": next_token,
            "top_k": [
                {"token": tok, "prob": prob.item()} 
                for tok, prob in zip(top_tokens, top_probs)
            ]
        }

        input_ids = torch.cat(
            [input_ids, next_token_id.view(1, 1)],
            dim=-1
        )