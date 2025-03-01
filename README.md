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
   - `GOOGLE_SERVICE_ACCOUNT_KEY`: The contents of your `key.json` file (base64 encoded)
   - `GOOGLE_API_KEY_GEMINI`: Your Gemini API key
   - `GOOGLE_DOC_ID`: Your Google Doc ID

The analysis results will be automatically written to your Google Doc.

## License

MIT 