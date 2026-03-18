from flask import Flask, request, jsonify, render_template, Response
from flask_cors import CORS
import json

from model_loader import load_model, get_available_models
from generator import generate_stepwise, generate_stepwise_stream

app = Flask(__name__)
CORS(app)

print("="*50)
print("TokViz - Token Generation Visualizer")
print("="*50)
print("\nPre-loading default model...")
# Pre-load the default model
load_model("gpt2")
print("\nServer ready! Models will be stored in ./models/ directory")
print("="*50)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = data.get("prompt", "")
    max_tokens = data.get("max_tokens", 10)
    top_k = data.get("top_k", 5)
    model_name = data.get("model_name", "gpt2")
    stream = data.get("stream", False)

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    
    if model_name not in get_available_models():
        return jsonify({"error": f"Model {model_name} not available"}), 400

    # Load the requested model (will use cache if already loaded)
    tokenizer, model = load_model(model_name)

    if stream:
        def generate_stream():
            for chunk in generate_stepwise_stream(
                model=model,
                tokenizer=tokenizer,
                prompt=prompt,
                max_new_tokens=max_tokens,
                top_k=top_k
            ):
                yield f"data: {json.dumps(chunk)}\n\n"
            yield "data: [DONE]\n\n"
        
        return Response(generate_stream(), mimetype='text/event-stream')
    else:
        result = generate_stepwise(
            model=model,
            tokenizer=tokenizer,
            prompt=prompt,
            max_new_tokens=max_tokens,
            top_k=top_k
        )
        return jsonify(result)


@app.route("/models", methods=["GET"])
def list_models():
    """Endpoint to get available models"""
    return jsonify({"models": get_available_models()})


@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)