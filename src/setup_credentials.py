import os
import sys
import webbrowser
from dotenv import load_dotenv

def main():
    """Guide the user through setting up Google Cloud credentials."""
    print("Google Cloud Credentials Setup Guide")
    print("===================================")
    print("\nThis script will help you set up the necessary credentials for the Productivity Tracker.")
    
    # Check if .env file exists and contains the GOOGLE_API_KEY_GEMINI
    load_dotenv()
    api_key = os.environ.get("GOOGLE_API_KEY_GEMINI")
    
    if api_key:
        print("\n✅ GOOGLE_API_KEY_GEMINI found in your .env file.")
    else:
        print("\n❌ GOOGLE_API_KEY_GEMINI not found in your .env file.")
        print("\nFollow these steps to get your Gemini API key:")
        print("1. Go to https://makersuite.google.com/app/apikey")
        print("2. Sign in with your Google account")
        print("3. Create a new API key or use an existing one")
        print("4. Add the API key to your .env file as GOOGLE_API_KEY_GEMINI=your-api-key")
        
        open_browser = input("\nWould you like to open the Gemini API key page in your browser? (y/n): ")
        if open_browser.lower() == "y":
            webbrowser.open("https://makersuite.google.com/app/apikey")
    
    print("\nNow, let's set up Google Application Default Credentials (ADC).")
    print("ADC is required to access the Google Docs API.")
    
    # Check if ADC is already set up
    adc_path = os.path.expanduser("~/.config/gcloud/application_default_credentials.json")
    if os.path.exists(adc_path):
        print("\n✅ Application Default Credentials found.")
    else:
        print("\n❌ Application Default Credentials not found.")
        print("\nFollow these steps to set up ADC:")
        print("1. Install the Google Cloud SDK: https://cloud.google.com/sdk/docs/install")
        print("2. Run the following command in your terminal:")
        print("   gcloud auth application-default login")
        print("3. Sign in with your Google account")
        print("4. Enable the Google Docs API in your Google Cloud project:")
        print("   - Go to https://console.cloud.google.com/apis/library/docs.googleapis.com")
        print("   - Select your project")
        print("   - Click 'Enable'")
        
        open_browser = input("\nWould you like to open the Google Cloud SDK installation page in your browser? (y/n): ")
        if open_browser.lower() == "y":
            webbrowser.open("https://cloud.google.com/sdk/docs/install")
    
    print("\nSetup guide complete! Once you have completed all the steps, you can run the Productivity Tracker:")
    print("python src/productivity_tracker.py")

if __name__ == "__main__":
    main() 