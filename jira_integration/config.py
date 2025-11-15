# jira-integration/config.py
from dotenv import load_dotenv
import os

load_dotenv()

JIRA_URL = "https://hafizatallah110.atlassian.net"
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_TOKEN = os.getenv("JIRA_TOKEN")
PROJECT_KEY = "KAN"   # ← Ganti dari "QA" ke "KAN" sesuai project kamu!
ISSUE_TYPE = "Task"