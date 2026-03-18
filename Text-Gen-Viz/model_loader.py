from transformers import AutoTokenizer, AutoModelForCausalLM
import os

# Set the models directory
MODELS_DIR = os.path.join(os.getcwd(), "models")

# Create models directory if it doesn't exist
os.makedirs(MODELS_DIR, exist_ok=True)

# Cache for loaded models to avoid reloading
_model_cache = {}

def load_model(model_name="gpt2"):
    """
    Load model and tokenizer, downloading to ./models/ directory if needed
    
    Args:
        model_name: Either "gpt2" or "distilgpt2"
    
    Returns:
        tuple: (tokenizer, model)
    """
    # Return from cache if already loaded
    if model_name in _model_cache:
        print(f"Using cached {model_name}")
        return _model_cache[model_name]
    
    print(f"Loading {model_name}...")
    
    # Set the cache directory to our models folder
    model_path = os.path.join(MODELS_DIR, model_name)
    
    # Load or download the model
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        cache_dir=MODELS_DIR,
        local_files_only=False
    )
    
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        cache_dir=MODELS_DIR,
        local_files_only=False
    )
    
    model.eval()
    
    # Cache the loaded model
    _model_cache[model_name] = (tokenizer, model)
    
    print(f"✓ {model_name} loaded successfully and cached in ./models/")
    
    return tokenizer, model

def get_available_models():
    """Return list of available model names"""
    return ["gpt2", "distilgpt2"]