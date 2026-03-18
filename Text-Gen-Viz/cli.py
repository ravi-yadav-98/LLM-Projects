from model_loader import load_model
from generator import generate_stepwise
from visualizer import print_step

def main():
    print("\n=== TokViz - Token-by-Token Visualization ===\n")

    prompt = input("Enter prompt: ")

    tokenizer, model = load_model("gpt2")

    result = generate_stepwise(
        model=model,
        tokenizer=tokenizer,
        prompt=prompt,
        max_new_tokens=10,
        top_k=5
    )

    print("\n" + "="*50)
    print("GENERATED TEXT:")
    print("="*50)
    print(result['full_text'])
    print("\n" + "="*50)
    print("TOKEN BREAKDOWN:")
    print("="*50)
    
    for i, token_data in enumerate(result['generated_tokens'], 1):
        print(f"\nStep {i}: {token_data['token']}")
        print("-" * 30)
        for item in token_data['top_k']:
            print(f"{item['token']:>15} : {item['prob']:.4f}")

if __name__ == "__main__":
    main()
