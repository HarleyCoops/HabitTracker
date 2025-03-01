import os
import sys
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np
from dotenv import load_dotenv
from data_parser import ProductivityDataParser
from productivity_tracker import read_google_doc

# Load environment variables from .env file
load_dotenv()

def create_mood_focus_chart(daily_logs):
    """
    Create a chart showing mood and focus over time.
    
    Args:
        daily_logs: A list of dictionaries, each representing a daily log.
        
    Returns:
        The figure object.
    """
    # Extract dates, moods, and focuses
    dates = []
    moods = []
    focuses = []
    
    for log in daily_logs:
        if 'date' in log and 'mood' in log and 'focus' in log:
            try:
                date = datetime.strptime(log['date'], '%B %d, %Y')
                dates.append(date)
                moods.append(log['mood'])
                focuses.append(log['focus'])
            except ValueError:
                # Skip logs with invalid dates
                continue
    
    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot mood and focus
    ax.plot(dates, moods, 'o-', color='blue', label='Mood')
    ax.plot(dates, focuses, 'o-', color='green', label='Focus')
    
    # Set the y-axis limits
    ax.set_ylim(0, 10)
    
    # Format the x-axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    plt.xticks(rotation=45)
    
    # Add labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Rating (0-10)')
    ax.set_title('Mood and Focus Over Time')
    
    # Add a legend
    ax.legend()
    
    # Add a grid
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Adjust layout
    plt.tight_layout()
    
    return fig

def create_achievements_challenges_chart(daily_logs):
    """
    Create a chart showing the number of achievements and challenges over time.
    
    Args:
        daily_logs: A list of dictionaries, each representing a daily log.
        
    Returns:
        The figure object.
    """
    # Extract dates, achievements, and challenges
    dates = []
    num_achievements = []
    num_challenges = []
    
    for log in daily_logs:
        if 'date' in log:
            try:
                date = datetime.strptime(log['date'], '%B %d, %Y')
                dates.append(date)
                
                # Count achievements
                if 'achievements' in log:
                    num_achievements.append(len(log['achievements']))
                else:
                    num_achievements.append(0)
                
                # Count challenges
                if 'challenges' in log:
                    num_challenges.append(len(log['challenges']))
                else:
                    num_challenges.append(0)
            except ValueError:
                # Skip logs with invalid dates
                continue
    
    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Set the width of the bars
    width = 0.35
    
    # Set the positions of the bars on the x-axis
    x = np.arange(len(dates))
    
    # Create the bars
    ax.bar(x - width/2, num_achievements, width, label='Achievements', color='blue')
    ax.bar(x + width/2, num_challenges, width, label='Challenges', color='red')
    
    # Format the x-axis
    ax.set_xticks(x)
    ax.set_xticklabels([date.strftime('%b %d') for date in dates], rotation=45)
    
    # Add labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Count')
    ax.set_title('Achievements and Challenges Over Time')
    
    # Add a legend
    ax.legend()
    
    # Add a grid
    ax.grid(True, linestyle='--', alpha=0.7, axis='y')
    
    # Adjust layout
    plt.tight_layout()
    
    return fig

def create_weekly_overview_chart(weekly_reviews):
    """
    Create a chart showing overall mood and productivity from weekly reviews.
    
    Args:
        weekly_reviews: A list of dictionaries, each representing a weekly review.
        
    Returns:
        The figure object.
    """
    # Extract weeks, overall moods, and overall productivities
    weeks = []
    overall_moods = []
    overall_productivities = []
    
    for review in weekly_reviews:
        if 'week' in review and 'overall_mood' in review and 'overall_productivity' in review:
            weeks.append(review['week'])
            overall_moods.append(review['overall_mood'])
            overall_productivities.append(review['overall_productivity'])
    
    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Set the width of the bars
    width = 0.35
    
    # Set the positions of the bars on the x-axis
    x = np.arange(len(weeks))
    
    # Create the bars
    ax.bar(x - width/2, overall_moods, width, label='Overall Mood', color='blue')
    ax.bar(x + width/2, overall_productivities, width, label='Overall Productivity', color='green')
    
    # Format the x-axis
    ax.set_xticks(x)
    ax.set_xticklabels(weeks, rotation=45)
    
    # Set the y-axis limits
    ax.set_ylim(0, 10)
    
    # Add labels and title
    ax.set_xlabel('Week')
    ax.set_ylabel('Rating (0-10)')
    ax.set_title('Weekly Overview: Mood and Productivity')
    
    # Add a legend
    ax.legend()
    
    # Add a grid
    ax.grid(True, linestyle='--', alpha=0.7, axis='y')
    
    # Adjust layout
    plt.tight_layout()
    
    return fig

def create_dashboard(doc_content):
    """
    Create a dashboard with multiple charts.
    
    Args:
        doc_content: The content of the Google Doc.
        
    Returns:
        None
    """
    # Create a parser instance
    parser = ProductivityDataParser()
    
    # Parse the data
    daily_logs = parser.parse_daily_logs(doc_content)
    weekly_reviews = parser.parse_weekly_reviews(doc_content)
    
    # Sort daily logs by date
    daily_logs.sort(key=lambda x: datetime.strptime(x.get('date', ''), '%B %d, %Y') if x.get('date') else datetime.min)
    
    # Create the charts
    mood_focus_fig = create_mood_focus_chart(daily_logs)
    achievements_challenges_fig = create_achievements_challenges_chart(daily_logs)
    weekly_overview_fig = create_weekly_overview_chart(weekly_reviews)
    
    # Show the charts
    plt.show()

def main():
    """Main function to run the dashboard."""
    print("Productivity and Mood Dashboard")
    print("==============================")
    
    # Check if document ID is provided as an environment variable
    document_id = os.environ.get("GOOGLE_DOC_ID")
    
    # If not, prompt the user for it
    if not document_id:
        document_id = input("Enter your Google Doc ID: ")
    
    # Read the Google Doc
    print("Reading Google Doc...")
    doc_content = read_google_doc(document_id)
    
    if not doc_content:
        print("Failed to read the Google Doc. Please check your credentials and document ID.")
        return
    
    # Create the dashboard
    print("Creating dashboard...")
    create_dashboard(doc_content)

if __name__ == "__main__":
    main() 