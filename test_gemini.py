import os
from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.environ.get("GOOGLE_API_KEY_GEMINI")
if not api_key:
    api_key = input("Enter your Gemini API key: ")

print(f"Using API key: {api_key[:10]}...")

# Configure the Gemini API with the new client approach
client = genai.Client(api_key=api_key)

# Test the API
try:
    # Try the gemini-2.0-flash model
    model_name = "gemini-2.0-flash"
    print(f"\nTrying model: {model_name}")
    
    response = client.models.generate_content(
        model=model_name,
        contents="Hello, how are you today?",
    )
    
    print("API Response:")
    print(response.text)
    print(f"API test successful with model {model_name}!")
    
except Exception as e:
    print(f"\nAPI Error: {e}") 