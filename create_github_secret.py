import json
import os
import sys

def main():
    # Path to the key.json file
    key_file_path = 'key.json'

    try:
        # Read the key.json file
        with open(key_file_path, 'r') as f:
            key_json = json.load(f)
        
        # Convert to a JSON string with minimal formatting
        # This creates a compact JSON string without unnecessary whitespace
        formatted_json = json.dumps(key_json, separators=(',', ':'))
        
        print("\n=== COPY THE FOLLOWING LINE FOR YOUR GITHUB SECRET ===")
        print(formatted_json)
        print("=== END OF SECRET VALUE ===\n")
        
        print("Instructions:")
        print("1. Copy the ENTIRE JSON string above (including the outer curly braces)")
        print("2. Go to your GitHub repository settings")
        print("3. Navigate to Secrets and Variables > Actions")
        print("4. Delete the existing GOOGLE_SERVICE_ACCOUNT_KEY secret")
        print("5. Create a new secret with the same name")
        print("6. Paste the copied JSON string as the value")
        print("7. Save the secret")
        print("8. Run the 'Verify Service Account Secret' workflow to test")
        
    except FileNotFoundError:
        print(f"Error: {key_file_path} not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: {key_file_path} contains invalid JSON: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
