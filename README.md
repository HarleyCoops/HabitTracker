# Productivity and Mood Tracker

This application helps you track your productivity and mood by analyzing your Google Docs entries and generating insights using Google's Gemini AI.

## Features

- Connect to Google Docs to read your productivity and mood data
- Generate weekly and monthly analyses using Google's Gemini AI
- Write the analyses back to your Google Doc
- Simple command-line interface

## Prerequisites

- Python 3.7 or higher
- Google Cloud account with the Google Docs API enabled
- Google API key for Gemini AI
- Google Application Default Credentials set up

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd HabitTracker
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   - Create a `.env` file in the root directory
   - Add your Google API key for Gemini AI:
     ```
     GOOGLE_API_KEY_GEMINI=your-api-key
     ```

4. Set up Google Application Default Credentials:
   - Follow the instructions at: https://cloud.google.com/docs/authentication/provide-credentials-adc

## Usage

1. Run the application:
   ```
   python src/productivity_tracker.py
   ```

2. Enter your Google Doc ID when prompted
3. Choose the type of analysis you want to generate (weekly, monthly, or both)
4. Review the generated analysis
5. Choose whether to write the analysis back to your Google Doc

## Google Doc Format

For best results, structure your Google Doc as follows:

### Daily Logs
```
Monday, March 1, 2023
- Mood: 8/10
- Focus: 7/10
- Achievements: Completed project X, started task Y
- Challenges: Distracted by social media
- Notes: Felt more productive in the morning

Tuesday, March 2, 2023
...
```

### Weekly Reviews
```
Week of March 1-7, 2023
- Overall mood: 7/10
- Overall productivity: 8/10
- Key achievements: Completed project X, made progress on Y
- Challenges: Struggled with focus on Wednesday and Thursday
- Goals for next week: Complete task Z, improve morning routine
```

## Future Enhancements

- Dashboard integration for data visualization
- Automated scheduling for regular analyses
- Support for different data formats
- Mobile app integration

## License

This project is licensed under the MIT License - see the LICENSE file for details. 