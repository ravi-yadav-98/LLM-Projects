# TokViz

**Token Generation Visualizer** - See how language models generate text token by token.

<!-- ![TokViz Demo](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg) -->

## What is TokViz?

TokViz is an educational tool that visualizes how transformer language models (like GPT-2) generate text one token at a time. Hover over any generated token to see the top alternatives the model considered and their probabilities.

## Features

- 🎯 **Token-by-Token Visualization** - See text generation in action
- 🔍 **Probability Inspection** - Hover over tokens to see top-k alternatives

## Installation

### Option 1: Docker (Recommended)

**Prerequisites:**
- Docker installed on your system

**Quick Start:**
```bash
# Clone the repository
git clone <your-repo-url>
cd TokViz

# Build the Docker image
docker build -t tokviz .

# Run the container
docker run -p 5000:5000 tokviz

# Access at http://localhost:5000
```

**Docker Commands:**
```bash
# Run with persistent model storage
docker run -p 5000:5000 -v $(pwd)/models:/app/models tokviz

# Run in detached mode
docker run -d -p 5000:5000 --name tokviz-app tokviz

# View logs
docker logs tokviz-app

# Stop and remove
docker stop tokviz-app
docker rm tokviz-app
```

### Option 2: Local Installation

**Prerequisites:**
- Python 3.8 or higher
- pip

**Setup:**

1. Clone the repository:
```bash
git clone <your-repo-url>
cd TokViz
```

2. Install dependencies:
```bash
pip install -r requirements.txt
# OR manually:
pip install flask flask-cors transformers torch
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and go to:
```
http://127.0.0.1:5000
```

## Usage

1. **Enter a prompt** in the text area
2. **Choose settings**:
   - Select model (GPT-2 or DistilGPT-2)
   - Set max tokens to generate
   - Set top-k value (1-20)
   - Toggle stream mode for real-time generation
3. **Click Generate**
4. **Hover over generated tokens** (dark gray) to see alternatives

## Project Structure

```
TokViz/
├── models/              # Auto-created, stores downloaded models
├── templates/
│   └── index.html       # Frontend UI
├── app.py               # Flask server
├── generator.py         # Token generation logic
├── model_loader.py      # Model loading and caching
├── visualizer.py        # CLI visualization (optional)
└── cli.py               # Command-line interface (optional)
```

## Models

- **GPT-2** (124M parameters) - Better quality, ~500MB
- **DistilGPT-2** (82M parameters) - Faster, smaller, ~250MB

Models are automatically downloaded to the `./models/` directory on first use.

## Requirements

```txt
flask>=3.0.0
flask-cors>=4.0.0
transformers>=4.30.0
torch>=2.0.0
```

## How It Works

1. User enters a prompt
2. Prompt is tokenized and fed to the model
3. Model predicts next token based on probabilities
4. Top-k candidates are shown on hover
5. Selected token is added and process repeats

## License

MIT License

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## Acknowledgments

- Built with [Transformers](https://huggingface.co/transformers/) by Hugging Face
- Models: GPT-2 by OpenAI, DistilGPT-2 by Hugging Face

---

Made with ❤️ for understanding language models better