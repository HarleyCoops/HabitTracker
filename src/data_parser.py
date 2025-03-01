import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

class ProductivityDataParser:
    """Parser for extracting structured data from productivity logs."""
    
    def __init__(self):
        """Initialize the parser."""
        # Regular expressions for parsing different parts of the log
        self.date_pattern = re.compile(r'(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})')
        self.week_pattern = re.compile(r'Week of ([A-Za-z]+\s+\d{1,2}-\d{1,2},\s+\d{4})')
        self.mood_pattern = re.compile(r'Mood:\s*(\d+(?:\.\d+)?)/10')
        self.focus_pattern = re.compile(r'Focus:\s*(\d+(?:\.\d+)?)/10')
        self.achievements_pattern = re.compile(r'Achievements:(.*?)(?=Challenges:|$)', re.DOTALL)
        self.challenges_pattern = re.compile(r'Challenges:(.*?)(?=Notes:|$)', re.DOTALL)
        self.notes_pattern = re.compile(r'Notes:(.*?)(?=\n\n|\Z)', re.DOTALL)
        
    def parse_daily_logs(self, text: str) -> List[Dict]:
        """
        Parse daily logs from the text.
        
        Args:
            text: The text containing daily logs.
            
        Returns:
            A list of dictionaries, each representing a daily log.
        """
        daily_logs = []
        
        # Split the text into daily entries
        days = re.split(r'\n\n(?=(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),)', text)
        
        for day in days:
            if not day.strip():
                continue
                
            log = {}
            
            # Extract date
            date_match = self.date_pattern.search(day)
            if date_match:
                day_of_week = date_match.group(1)
                date_str = date_match.group(2)
                log['day_of_week'] = day_of_week
                log['date'] = date_str
            
            # Extract mood
            mood_match = self.mood_pattern.search(day)
            if mood_match:
                log['mood'] = float(mood_match.group(1))
            
            # Extract focus
            focus_match = self.focus_pattern.search(day)
            if focus_match:
                log['focus'] = float(focus_match.group(1))
            
            # Extract achievements
            achievements_match = self.achievements_pattern.search(day)
            if achievements_match:
                achievements = achievements_match.group(1).strip()
                log['achievements'] = [a.strip() for a in achievements.split('-') if a.strip()]
            
            # Extract challenges
            challenges_match = self.challenges_pattern.search(day)
            if challenges_match:
                challenges = challenges_match.group(1).strip()
                log['challenges'] = [c.strip() for c in challenges.split('-') if c.strip()]
            
            # Extract notes
            notes_match = self.notes_pattern.search(day)
            if notes_match:
                log['notes'] = notes_match.group(1).strip()
            
            if log:  # Only add if we extracted something
                daily_logs.append(log)
        
        return daily_logs
    
    def parse_weekly_reviews(self, text: str) -> List[Dict]:
        """
        Parse weekly reviews from the text.
        
        Args:
            text: The text containing weekly reviews.
            
        Returns:
            A list of dictionaries, each representing a weekly review.
        """
        weekly_reviews = []
        
        # Split the text into weekly entries
        weeks = re.split(r'\n\n(?=Week of)', text)
        
        for week in weeks:
            if not week.strip():
                continue
                
            review = {}
            
            # Extract week
            week_match = self.week_pattern.search(week)
            if week_match:
                review['week'] = week_match.group(1)
            
            # Extract overall mood
            overall_mood_match = re.search(r'Overall mood:\s*(\d+(?:\.\d+)?)/10', week)
            if overall_mood_match:
                review['overall_mood'] = float(overall_mood_match.group(1))
            
            # Extract overall productivity
            overall_productivity_match = re.search(r'Overall productivity:\s*(\d+(?:\.\d+)?)/10', week)
            if overall_productivity_match:
                review['overall_productivity'] = float(overall_productivity_match.group(1))
            
            # Extract key achievements
            key_achievements_match = re.search(r'Key achievements:(.*?)(?=Challenges:|$)', week, re.DOTALL)
            if key_achievements_match:
                achievements = key_achievements_match.group(1).strip()
                review['key_achievements'] = [a.strip() for a in achievements.split('-') if a.strip()]
            
            # Extract challenges
            challenges_match = re.search(r'Challenges:(.*?)(?=Goals for next week:|$)', week, re.DOTALL)
            if challenges_match:
                challenges = challenges_match.group(1).strip()
                review['challenges'] = [c.strip() for c in challenges.split('-') if c.strip()]
            
            # Extract goals for next week
            goals_match = re.search(r'Goals for next week:(.*?)(?=\n\n|\Z)', week, re.DOTALL)
            if goals_match:
                goals = goals_match.group(1).strip()
                review['goals_for_next_week'] = [g.strip() for g in goals.split('-') if g.strip()]
            
            if review:  # Only add if we extracted something
                weekly_reviews.append(review)
        
        return weekly_reviews
    
    def extract_data_for_analysis(self, text: str, analysis_type: str = "weekly") -> Dict:
        """
        Extract data for analysis based on the analysis type.
        
        Args:
            text: The text containing productivity data.
            analysis_type: The type of analysis to perform ("weekly" or "monthly").
            
        Returns:
            A dictionary containing the extracted data.
        """
        data = {}
        
        if analysis_type == "weekly":
            # For weekly analysis, extract data from the past 7 days
            daily_logs = self.parse_daily_logs(text)
            
            # Sort logs by date
            daily_logs.sort(key=lambda x: datetime.strptime(x.get('date', ''), '%B %d, %Y') if x.get('date') else datetime.min)
            
            # Get logs from the past 7 days
            today = datetime.now()
            seven_days_ago = today - timedelta(days=7)
            
            recent_logs = [
                log for log in daily_logs 
                if log.get('date') and datetime.strptime(log['date'], '%B %d, %Y') >= seven_days_ago
            ]
            
            data['daily_logs'] = recent_logs
            
            # Also include the most recent weekly review if available
            weekly_reviews = self.parse_weekly_reviews(text)
            if weekly_reviews:
                data['weekly_review'] = weekly_reviews[-1]
                
        elif analysis_type == "monthly":
            # For monthly analysis, extract data from the past 30 days
            daily_logs = self.parse_daily_logs(text)
            
            # Sort logs by date
            daily_logs.sort(key=lambda x: datetime.strptime(x.get('date', ''), '%B %d, %Y') if x.get('date') else datetime.min)
            
            # Get logs from the past 30 days
            today = datetime.now()
            thirty_days_ago = today - timedelta(days=30)
            
            recent_logs = [
                log for log in daily_logs 
                if log.get('date') and datetime.strptime(log['date'], '%B %d, %Y') >= thirty_days_ago
            ]
            
            data['daily_logs'] = recent_logs
            
            # Include all weekly reviews from the past 30 days
            weekly_reviews = self.parse_weekly_reviews(text)
            
            recent_reviews = []
            for review in weekly_reviews:
                if review.get('week'):
                    # Extract the end date from the week string (e.g., "March 1-7, 2023" -> "March 7, 2023")
                    week_str = review['week']
                    match = re.search(r'([A-Za-z]+)\s+\d{1,2}-(\d{1,2}),\s+(\d{4})', week_str)
                    if match:
                        month, day, year = match.group(1), match.group(2), match.group(3)
                        end_date_str = f"{month} {day}, {year}"
                        try:
                            end_date = datetime.strptime(end_date_str, '%B %d, %Y')
                            if end_date >= thirty_days_ago:
                                recent_reviews.append(review)
                        except ValueError:
                            # If date parsing fails, include the review anyway
                            recent_reviews.append(review)
                    else:
                        # If regex doesn't match, include the review anyway
                        recent_reviews.append(review)
            
            data['weekly_reviews'] = recent_reviews
        
        return data
    
    def format_data_for_gemini(self, data: Dict, analysis_type: str = "weekly") -> str:
        """
        Format the extracted data for the Gemini API.
        
        Args:
            data: The extracted data.
            analysis_type: The type of analysis to perform ("weekly" or "monthly").
            
        Returns:
            A formatted string for the Gemini API.
        """
        formatted_text = ""
        
        if analysis_type == "weekly":
            # Format daily logs
            if 'daily_logs' in data and data['daily_logs']:
                formatted_text += "Daily Logs:\n\n"
                
                for log in data['daily_logs']:
                    formatted_text += f"{log.get('day_of_week', 'Unknown')}, {log.get('date', 'Unknown')}\n"
                    formatted_text += f"- Mood: {log.get('mood', 'N/A')}/10\n"
                    formatted_text += f"- Focus: {log.get('focus', 'N/A')}/10\n"
                    
                    if 'achievements' in log:
                        formatted_text += "- Achievements:\n"
                        for achievement in log['achievements']:
                            formatted_text += f"  - {achievement}\n"
                    
                    if 'challenges' in log:
                        formatted_text += "- Challenges:\n"
                        for challenge in log['challenges']:
                            formatted_text += f"  - {challenge}\n"
                    
                    if 'notes' in log:
                        formatted_text += f"- Notes: {log['notes']}\n"
                    
                    formatted_text += "\n"
            
            # Format weekly review if available
            if 'weekly_review' in data:
                review = data['weekly_review']
                formatted_text += "Weekly Review:\n\n"
                formatted_text += f"Week of {review.get('week', 'Unknown')}\n"
                formatted_text += f"- Overall mood: {review.get('overall_mood', 'N/A')}/10\n"
                formatted_text += f"- Overall productivity: {review.get('overall_productivity', 'N/A')}/10\n"
                
                if 'key_achievements' in review:
                    formatted_text += "- Key achievements:\n"
                    for achievement in review['key_achievements']:
                        formatted_text += f"  - {achievement}\n"
                
                if 'challenges' in review:
                    formatted_text += "- Challenges:\n"
                    for challenge in review['challenges']:
                        formatted_text += f"  - {challenge}\n"
                
                if 'goals_for_next_week' in review:
                    formatted_text += "- Goals for next week:\n"
                    for goal in review['goals_for_next_week']:
                        formatted_text += f"  - {goal}\n"
        
        elif analysis_type == "monthly":
            # Format daily logs (summarized)
            if 'daily_logs' in data and data['daily_logs']:
                # Calculate average mood and focus
                moods = [log.get('mood') for log in data['daily_logs'] if 'mood' in log]
                focuses = [log.get('focus') for log in data['daily_logs'] if 'focus' in log]
                
                avg_mood = sum(moods) / len(moods) if moods else 'N/A'
                avg_focus = sum(focuses) / len(focuses) if focuses else 'N/A'
                
                formatted_text += "Monthly Summary:\n\n"
                formatted_text += f"- Number of days logged: {len(data['daily_logs'])}\n"
                formatted_text += f"- Average mood: {avg_mood:.1f}/10\n" if isinstance(avg_mood, float) else f"- Average mood: {avg_mood}\n"
                formatted_text += f"- Average focus: {avg_focus:.1f}/10\n" if isinstance(avg_focus, float) else f"- Average focus: {avg_focus}\n"
                
                # Collect all achievements and challenges
                all_achievements = []
                all_challenges = []
                
                for log in data['daily_logs']:
                    if 'achievements' in log:
                        all_achievements.extend(log['achievements'])
                    if 'challenges' in log:
                        all_challenges.extend(log['challenges'])
                
                # Remove duplicates
                unique_achievements = list(set(all_achievements))
                unique_challenges = list(set(all_challenges))
                
                if unique_achievements:
                    formatted_text += "- Key achievements this month:\n"
                    for achievement in unique_achievements[:10]:  # Limit to top 10
                        formatted_text += f"  - {achievement}\n"
                
                if unique_challenges:
                    formatted_text += "- Key challenges this month:\n"
                    for challenge in unique_challenges[:10]:  # Limit to top 10
                        formatted_text += f"  - {challenge}\n"
                
                formatted_text += "\n"
            
            # Format weekly reviews
            if 'weekly_reviews' in data and data['weekly_reviews']:
                formatted_text += "Weekly Reviews:\n\n"
                
                for review in data['weekly_reviews']:
                    formatted_text += f"Week of {review.get('week', 'Unknown')}\n"
                    formatted_text += f"- Overall mood: {review.get('overall_mood', 'N/A')}/10\n"
                    formatted_text += f"- Overall productivity: {review.get('overall_productivity', 'N/A')}/10\n"
                    
                    if 'key_achievements' in review:
                        formatted_text += "- Key achievements:\n"
                        for achievement in review['key_achievements']:
                            formatted_text += f"  - {achievement}\n"
                    
                    if 'challenges' in review:
                        formatted_text += "- Challenges:\n"
                        for challenge in review['challenges']:
                            formatted_text += f"  - {challenge}\n"
                    
                    if 'goals_for_next_week' in review:
                        formatted_text += "- Goals:\n"
                        for goal in review['goals_for_next_week']:
                            formatted_text += f"  - {goal}\n"
                    
                    formatted_text += "\n"
        
        return formatted_text

# Example usage
if __name__ == "__main__":
    # Sample text for testing
    sample_text = """
    Monday, March 1, 2023
    - Mood: 8/10
    - Focus: 7/10
    - Achievements: Completed project X, started task Y
    - Challenges: Distracted by social media
    - Notes: Felt more productive in the morning

    Tuesday, March 2, 2023
    - Mood: 7/10
    - Focus: 6/10
    - Achievements: Made progress on task Y, had a good meeting with team
    - Challenges: Struggled with focus in the afternoon
    - Notes: Need to improve time management

    Week of March 1-7, 2023
    - Overall mood: 7/10
    - Overall productivity: 8/10
    - Key achievements: Completed project X, made progress on Y
    - Challenges: Struggled with focus on Wednesday and Thursday
    - Goals for next week: Complete task Z, improve morning routine
    """
    
    parser = ProductivityDataParser()
    
    # Parse daily logs
    daily_logs = parser.parse_daily_logs(sample_text)
    print("Daily Logs:")
    for log in daily_logs:
        print(log)
    
    # Parse weekly reviews
    weekly_reviews = parser.parse_weekly_reviews(sample_text)
    print("\nWeekly Reviews:")
    for review in weekly_reviews:
        print(review)
    
    # Extract data for weekly analysis
    weekly_data = parser.extract_data_for_analysis(sample_text, "weekly")
    formatted_weekly_data = parser.format_data_for_gemini(weekly_data, "weekly")
    print("\nFormatted Weekly Data:")
    print(formatted_weekly_data)
    
    # Extract data for monthly analysis
    monthly_data = parser.extract_data_for_analysis(sample_text, "monthly")
    formatted_monthly_data = parser.format_data_for_gemini(monthly_data, "monthly")
    print("\nFormatted Monthly Data:")
    print(formatted_monthly_data) 