import os
import sys
import webbrowser
from dotenv import load_dotenv

def main():
    """Guide the user through updating Google Cloud project settings."""
    print("Google Cloud Project Update Guide")
    print("================================")
    print("\nThis script will help you update your Google Cloud project settings for the Productivity Tracker.")
    
    # Load environment variables
    load_dotenv()
    
    # Check if project info is in .env file
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    project_number = os.environ.get("GOOGLE_CLOUD_PROJECT_NUMBER")
    api_key = os.environ.get("GOOGLE_API_KEY_GEMINI")
    
    if project_id and project_number:
        print(f"\n✅ Google Cloud Project information found:")
        print(f"   Project ID: {project_id}")
        print(f"   Project Number: {project_number}")
    else:
        print("\n❌ Google Cloud Project information not found in your .env file.")
        print("   Please add the following to your .env file:")
        print("   GOOGLE_CLOUD_PROJECT_ID=habittracker-452412")
        print("   GOOGLE_CLOUD_PROJECT_NUMBER=235429790574")
    
    if api_key:
        print(f"\n✅ GOOGLE_API_KEY_GEMINI found in your .env file.")
    else:
        print("\n❌ GOOGLE_API_KEY_GEMINI not found in your .env file.")
        print("   Please add your Gemini API key to your .env file.")
    
    print("\nTo update your Google Cloud project settings, follow these steps:")
    print("1. Go to the Google Cloud Console: https://console.cloud.google.com/")
    print("2. Select the project 'habittracker-452412'")
    print("3. Enable the necessary APIs:")
    print("   - Google Docs API")
    print("   - Gemini API")
    
    open_browser = input("\nWould you like to open the Google Cloud Console in your browser? (y/n): ")
    if open_browser.lower() == "y":
        webbrowser.open("https://console.cloud.google.com/")
    
    print("\nTo update your Application Default Credentials (ADC) for the new project:")
    print("1. Run the following command in your terminal:")
    print("   gcloud auth application-default login --project=habittracker-452412")
    print("2. Sign in with your Google account")
    
    print("\nUpdate complete! You can now run the Productivity Tracker with the new project settings.")

if __name__ == "__main__":
    main() 