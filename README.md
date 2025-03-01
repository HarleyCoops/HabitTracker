# Productivity and Mood Tracker

A tool to track and analyze your productivity and mood data from Google Docs using AI-powered insights.

## Features

- Read productivity and mood data from Google Docs
- Generate AI-powered weekly and monthly analysis using Google's Gemini AI
- Write analysis back to your Google Doc
- Automated analysis via GitHub Actions

## Setup

### Prerequisites

- Python 3.8+
- A Google Cloud Project with the following APIs enabled:
  - Google Docs API
  - Google Drive API
  - Gemini AI API
- A Google Doc containing your productivity and mood data

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/HarleyCoops/HabitTracker.git
   cd HabitTracker
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your configuration:
   ```
   GOOGLE_API_KEY_GEMINI=your_gemini_api_key
   GOOGLE_DOC_ID=your_google_doc_id
   ```

4. Set up Google Cloud service account:
   - Create a service account in Google Cloud Console
   - Grant it access to your Google Doc
   - Download the service account key as `key.json`

## Usage

### Manual Analysis

Run the analysis manually:

```
python src/main.py --analyze
```

Options:
- `--doc-id`: Specify a Google Doc ID
- `--analysis-type`: Choose "weekly", "monthly", or "both"
- `--write-to-doc`: Automatically write analysis to the Google Doc
- `--automated`: Run in automated mode without user prompts

### Automated Analysis with GitHub Actions

This repository includes GitHub Actions workflows that automatically run weekly and monthly analyses:

1. Weekly analysis: Runs every Sunday at 8:00 PM UTC
2. Monthly analysis: Runs on the 1st of each month at 8:00 PM UTC

To set up GitHub Actions:

1. Fork this repository
2. Add the following secrets to your GitHub repository:
   - `GOOGLE_SERVICE_ACCOUNT_KEY`: The contents of your `key.json` file (as a properly formatted JSON string)
   - `GOOGLE_API_KEY_GEMINI`: Your Gemini API key
   - `GOOGLE_DOC_ID`: Your Google Doc ID

The analysis results will be automatically written to your Google Doc.

## GitHub Workflows

This repository contains three GitHub workflow files that handle different aspects of the automation:

### 1. Scheduled Productivity Analysis (`scheduled-analysis.yml`)

This is the main workflow that runs on a schedule to analyze your productivity data and write the results back to your Google Doc.

- **Schedule**: Runs weekly (Sundays at 8:00 PM UTC) and monthly (1st of each month at 8:00 PM UTC)
- **Manual Trigger**: Can also be triggered manually via the GitHub Actions UI
- **What it does**: 
  - Checks out the code
  - Sets up Python
  - Installs dependencies
  - Creates a service account key file from the GitHub secret
  - Sets up environment variables
  - Determines whether to run weekly or monthly analysis based on the date
  - Runs the analysis and writes the results to your Google Doc

### 2. Test Google API Authentication (`test-auth.yml`)

This workflow is used to test if the Google API authentication is working correctly.

- **Trigger**: Manual only (via GitHub Actions UI)
- **What it does**:
  - Checks out the code
  - Sets up Python
  - Installs necessary dependencies
  - Creates a test key file from the GitHub secret
  - Validates that the key file contains valid JSON
  - Runs a Python script to test authentication with the Google Docs API
  - Attempts to access the specified Google Doc

### 3. Verify Service Account Secret (`verify-secret.yml`)

This workflow is used to verify that the `GOOGLE_SERVICE_ACCOUNT_KEY` secret is properly formatted.

- **Trigger**: Manual only (via GitHub Actions UI)
- **What it does**:
  - Creates a temporary key file from the GitHub secret
  - Checks if it's valid JSON
  - Verifies that it contains the expected service account fields
  - Displays the project ID and client email for verification

## Helper Scripts

This repository includes several helper scripts to assist with managing the service account key:

### 1. `create_github_secret.py`

A utility script to help format your service account key for use as a GitHub secret.

- **Usage**: `python create_github_secret.py`
- **What it does**: 
  - Reads your local `key.json` file
  - Formats it as a compact JSON string
  - Outputs the formatted string to the console for copying
  - Provides instructions for adding it as a GitHub secret

### 2. `create_compact_key.py`

A utility script that creates a compact version of your service account key.

- **Usage**: `python create_compact_key.py`
- **What it does**:
  - Reads your local `key.json` file
  - Creates a compact JSON version without extra whitespace
  - Saves it to `github_secret.txt` for easy copying

### 3. `copy_key_to_clipboard.py`

A utility script to copy your service account key to the clipboard.

- **Usage**: `python copy_key_to_clipboard.py`
- **What it does**:
  - Reads your local `key.json` file
  - Formats it as a JSON string
  - Outputs it to the console for copying

## Core Scripts

This repository contains several Python scripts in the `src/` directory that handle different aspects of the productivity tracking and analysis:

### 1. `main.py`

The main entry point for the application that parses command-line arguments and calls the appropriate functions.

- **Usage**: `python src/main.py [options]`
- **Key Functions**:
  - Parses command-line arguments
  - Loads environment variables
  - Calls the appropriate module based on the arguments (setup, update project, analyze, dashboard)

### 2. `productivity_tracker.py`

The core module that handles reading from Google Docs, generating analysis, and writing back to the document.

- **Key Functions**:
  - `authenticate_google_docs_api()`: Authenticates with the Google Docs API
  - `read_google_doc()`: Reads content from a Google Doc
  - `generate_analysis_with_gemini()`: Generates analysis using the Gemini AI
  - `write_analysis_to_doc()`: Writes the analysis back to the Google Doc
  - `main()`: Orchestrates the entire process

### 3. `data_parser.py`

Handles parsing and formatting the productivity data from the Google Doc.

- **Key Functions**:
  - `extract_data_for_analysis()`: Extracts relevant data for weekly or monthly analysis
  - `format_data_for_gemini()`: Formats the extracted data for the Gemini AI

### 4. `setup_credentials.py`

Helps with setting up the necessary credentials for the application.

- **Key Functions**:
  - Guides the user through setting up Google Cloud credentials
  - Creates the necessary environment variables

### 5. `update_project.py`

Handles updating the Google Cloud project settings.

- **Key Functions**:
  - Updates API enablement
  - Configures service account permissions

### 6. `dashboard.py`

Provides a visual dashboard for the productivity data.

- **Key Functions**:
  - Visualizes productivity and mood trends
  - Displays insights from the analysis

## Troubleshooting

### GitHub Actions Authentication Issues

If you encounter authentication issues with GitHub Actions, try the following:

1. **Verify the Secret Format**:
   - Run the "Verify Service Account Secret" workflow to check if your secret is valid JSON
   - Make sure the `GOOGLE_SERVICE_ACCOUNT_KEY` secret contains the entire JSON content of your service account key
   - Use the `create_compact_key.py` script to generate a properly formatted JSON string

2. **Check Service Account Permissions**:
   - Ensure your service account has access to the Google Doc
   - Share your Google Doc with the service account email (found in the `client_email` field of your key.json)
   - Grant the service account "Editor" permissions on the Google Doc

3. **API Enablement**:
   - Make sure the Google Docs API and Google Drive API are enabled in your Google Cloud project
   - Use the `update_project.py` script to enable the necessary APIs

4. **Secret Handling in Workflows**:
   - If you modify the workflow files, be careful with how you handle the secret
   - Use proper quoting when writing the secret to a file
   - Validate the JSON before using it

### Local Authentication Issues

If you encounter authentication issues when running locally:

1. **Check your key.json file**:
   - Make sure the key.json file is in the root directory of the project
   - Verify that it contains valid JSON
   - Ensure it has the necessary fields (type, project_id, private_key, client_email, etc.)

2. **Environment Variables**:
   - Check that your .env file contains the necessary variables
   - Verify that the GOOGLE_DOC_ID is correct
   - Make sure the GOOGLE_API_KEY_GEMINI is valid

3. **Google Doc Access**:
   - Ensure your service account has access to the Google Doc
   - Check that the Google Doc ID is correct

## License

MIT
