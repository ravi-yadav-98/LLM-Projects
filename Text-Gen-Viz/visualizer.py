def print_step(step_data):
    print(f"\nStep {step_data['step']}")
    print("-" * 30)

    for token, prob in step_data["top_tokens"]:
        token_display = token.replace("Ġ", "␣")  # GPT-2 space marker
        print(f"{token_display:>10} : {prob:.4f}")

    print(f"\nChosen token → {step_data['chosen_token']}")