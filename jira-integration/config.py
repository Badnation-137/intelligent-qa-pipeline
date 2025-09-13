from dotenv import load_dotenv
import os

load_dotenv()

JIRA_URL = "https://hafizatata811-1757750605657.atlassian.net"
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_TOKEN = os.getenv("JIRA_TOKEN")
PROJECT_KEY = "SCRUM"
ISSUE_TYPE = "Task"