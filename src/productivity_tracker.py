import os
import sys
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google import genai
from dotenv import load_dotenv
from data_parser import ProductivityDataParser
from google.oauth2 import service_account

# Load environment variables from .env file
load_dotenv()

# Get the Google API key from environment variables
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY_GEMINI")
if not GOOGLE_API_KEY:
    print("Error: GOOGLE_API_KEY_GEMINI environment variable is not set.")
    sys.exit(1)

# Print the API key (first few characters) for debugging
print(f"Gemini API Key found: {GOOGLE_API_KEY[:10]}...")

# Configure the Gemini API with the new client approach
genai_client = genai.Client(api_key=GOOGLE_API_KEY)

def authenticate_google_docs_api():
    """Authenticates with the Google Docs API and returns the service."""
    creds = None

    try:
        # Check if service account key file exists
        if os.path.exists('key.json'):
            # Use service account credentials
            SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']
            creds = service_account.Credentials.from_service_account_file('key.json', scopes=SCOPES)
            print("Using service account authentication")
        else:
            # Fall back to Application Default Credentials
            print("Service account key file not found, falling back to Application Default Credentials")
            creds, project = google.auth.default()
    except Exception as e:
        print(f"Authentication error: {e}")
        return None

    try:
        service = build('docs', 'v1', credentials=creds)
        return service
    except HttpError as err:
        print(f"An error occurred: {err}")
        return None

def read_google_doc(document_id):
    """Reads the content of a Google Doc and returns it as a string."""
    service = authenticate_google_docs_api()
    if not service:
        return None

    try:
        document = service.documents().get(documentId=document_id).execute()
        content = document.get('body').get('content')

        text = ""
        for element in content:
            if 'paragraph' in element:
                for run in element['paragraph']['elements']:
                    if 'textRun' in run:
                        text += run['textRun']['content']
        return text

    except HttpError as err:
        print(f"An error occurred: {err}")
        return None

def generate_analysis_with_gemini(data, analysis_type="weekly"):
    """
    Generates weekly or monthly analysis using the Gemini API.

    Args:
        data: The data (e.g., daily logs) as a string.
        analysis_type: "weekly" or "monthly" (string)

    Returns:
        A string containing the analysis from Gemini.
    """
    if analysis_type == "weekly":
        prompt = f"""Analyze the following weekly productivity and mood data:

        {data}

        Provide a concise summary of achievements, challenges, patterns in mood/focus, and adjustments for the next week. Be specific and offer actionable advice for improvements. Provide a short analysis of around 50-75 words only."""

    elif analysis_type == "monthly":
        prompt = f"""Analyze the following monthly productivity and mood data:

        {data}

        Provide an overall summary of achievements, key patterns/observations, biggest lessons learned, and goals for the next month. Be specific and offer actionable advice for continued progress. Provide a short analysis of around 75-100 words only."""
    else:
        return "Error: Invalid analysis_type. Must be 'weekly' or 'monthly'."

    try:
        response = genai_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text

    except Exception as e:
        print(f"Error during Gemini API call: {e}")
        return None

def write_analysis_to_doc(document_id, analysis, analysis_type):
    """Writes the Gemini-generated analysis to the Google Doc."""

    service = authenticate_google_docs_api()
    if not service:
        return

    try:
        # Create structured analysis by type to append as a section of content.
        if analysis_type == "weekly":
            section_title = "Weekly Analysis"
        elif analysis_type == "monthly":
            section_title = "Monthly Analysis"
        else:
            return "Error: Invalid analysis_type. Must be 'weekly' or 'monthly'."

        # Basic structure to contain the title as a heading and the analysis text below the title.
        requests = [
            {
                'insertText': {
                    'location': {
                        'index': 1  # Beginning of the document. Adjust if needed.
                    },
                    'text': section_title + "\n",
                }
            },
            {
                'updateTextStyle': {  # Add this new request for title as heading
                    'range': {
                        'startIndex': 1,
                        'endIndex': len(section_title) + 2,
                    },
                    'textStyle': {
                        'bold': True,
                        'fontSize': {
                            'magnitude': 16,
                            'unit': 'PT'
                        }
                    },
                    'fields': 'bold,fontSize'  # only the requested modifications
                }
            },
            {
                'insertText': {
                    'location': {
                        'index': len(section_title) + 2  # After the title
                    },
                    'text': analysis + "\n\n",
                }
            },
        ]
        result = service.documents().batchUpdate(documentId=document_id,
                                                body={'requests': requests}).execute()
        print(f"Updated document {document_id} with {analysis_type} analysis")
        return result
    except HttpError as err:
        print(f"An error occurred: {err}")

def main(automated=False):
    """Main function to run the productivity tracker."""
    print("Productivity and Mood Tracker")
    print("============================")
    
    # Check if document ID is provided as an environment variable
    document_id = os.environ.get("GOOGLE_DOC_ID")
    
    # If not, prompt the user for it
    if not document_id:
        if automated:
            print("Error: GOOGLE_DOC_ID environment variable is not set.")
            return
        document_id = input("Enter your Google Doc ID: ")
    
    # Read the Google Doc
    print("Reading Google Doc...")
    doc_content = read_google_doc(document_id)
    
    if not doc_content:
        print("Failed to read the Google Doc. Please check your credentials and document ID.")
        return
    
    # Create a parser instance
    parser = ProductivityDataParser()
    
    # Check if analysis type is provided as an environment variable
    analysis_type = os.environ.get("ANALYSIS_TYPE", "both")
    
    # If not, prompt the user for it
    if analysis_type not in ["weekly", "monthly", "both"]:
        if automated:
            analysis_type = "both"
        else:
            print("\nWhat type of analysis would you like to generate?")
            print("1. Weekly Analysis")
            print("2. Monthly Analysis")
            print("3. Both")
            
            choice = input("Enter your choice (1-3): ")
            
            if choice == "1":
                analysis_type = "weekly"
            elif choice == "2":
                analysis_type = "monthly"
            else:
                analysis_type = "both"
    
    # Check if write-to-doc is provided as an environment variable
    write_to_doc = os.environ.get("WRITE_TO_DOC", "").lower() == "true"
    
    # In automated mode, always write to doc
    if automated:
        write_to_doc = True
    
    if analysis_type == "weekly" or analysis_type == "both":
        print("\nGenerating weekly analysis...")
        
        # Extract and format data for weekly analysis
        weekly_data = parser.extract_data_for_analysis(doc_content, "weekly")
        formatted_weekly_data = parser.format_data_for_gemini(weekly_data, "weekly")
        
        # Generate weekly analysis
        weekly_analysis = generate_analysis_with_gemini(formatted_weekly_data, "weekly")
        
        if weekly_analysis:
            print("\nWeekly Analysis:")
            print(weekly_analysis)
            
            if not write_to_doc and not automated:
                write_to_doc_input = input("\nWould you like to write this analysis to your Google Doc? (y/n): ")
                write_to_doc = write_to_doc_input.lower() == "y"
            
            if write_to_doc:
                write_analysis_to_doc(document_id, weekly_analysis, "weekly")
                print("Weekly analysis written to document.")
    
    if analysis_type == "monthly" or analysis_type == "both":
        print("\nGenerating monthly analysis...")
        
        # Extract and format data for monthly analysis
        monthly_data = parser.extract_data_for_analysis(doc_content, "monthly")
        formatted_monthly_data = parser.format_data_for_gemini(monthly_data, "monthly")
        
        # Generate monthly analysis
        monthly_analysis = generate_analysis_with_gemini(formatted_monthly_data, "monthly")
        
        if monthly_analysis:
            print("\nMonthly Analysis:")
            print(monthly_analysis)
            
            if not write_to_doc and not automated:
                write_to_doc_input = input("\nWould you like to write this analysis to your Google Doc? (y/n): ")
                write_to_doc = write_to_doc_input.lower() == "y"
            
            if write_to_doc:
                write_analysis_to_doc(document_id, monthly_analysis, "monthly")
                print("Monthly analysis written to document.")
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main() 