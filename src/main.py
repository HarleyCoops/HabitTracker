import os
import sys
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def main():
    """Main entry point for the Productivity and Mood Tracker application."""
    parser = argparse.ArgumentParser(description="Productivity and Mood Tracker")
    parser.add_argument("--setup", action="store_true", help="Run the setup script to configure credentials")
    parser.add_argument("--update-project", action="store_true", help="Update Google Cloud project settings")
    parser.add_argument("--analyze", action="store_true", help="Run the productivity tracker to analyze your data")
    parser.add_argument("--dashboard", action="store_true", help="Run the dashboard to visualize your data")
    parser.add_argument("--doc-id", type=str, help="Google Doc ID to analyze")
    parser.add_argument("--analysis-type", type=str, choices=["weekly", "monthly", "both"], default="both",
                        help="Type of analysis to generate (weekly, monthly, or both)")
    parser.add_argument("--write-to-doc", action="store_true", help="Write the analysis back to the Google Doc")
    
    args = parser.parse_args()
    
    if args.setup:
        # Import and run the setup script
        from setup_credentials import main as setup_main
        setup_main()
    
    elif args.update_project:
        # Import and run the update project script
        from update_project import main as update_project_main
        update_project_main()
    
    elif args.analyze:
        # Import and run the productivity tracker
        from productivity_tracker import main as tracker_main
        
        # If a doc ID was provided, set it as an environment variable
        if args.doc_id:
            os.environ["GOOGLE_DOC_ID"] = args.doc_id
        
        # If an analysis type was provided, set it as an environment variable
        if args.analysis_type:
            os.environ["ANALYSIS_TYPE"] = args.analysis_type
        
        # If write-to-doc was provided, set it as an environment variable
        if args.write_to_doc:
            os.environ["WRITE_TO_DOC"] = "true"
        
        tracker_main()
    
    elif args.dashboard:
        # Import and run the dashboard
        from dashboard import main as dashboard_main
        
        # If a doc ID was provided, set it as an environment variable
        if args.doc_id:
            os.environ["GOOGLE_DOC_ID"] = args.doc_id
        
        dashboard_main()
    
    else:
        # If no arguments were provided, show the help message
        parser.print_help()

if __name__ == "__main__":
    main() 