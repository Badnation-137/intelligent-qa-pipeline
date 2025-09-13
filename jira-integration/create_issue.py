# jira-integration/create_issue.py

import requests
import json
from config import JIRA_URL, JIRA_EMAIL, JIRA_TOKEN, PROJECT_KEY, ISSUE_TYPE

def create_jira_task(summary, description_text, priority="Medium"):
    """
    Buat task baru di Jira dengan format ADF untuk deskripsi
    """
    url = f"{JIRA_URL}/rest/api/3/issue"
    
    auth = (JIRA_EMAIL, JIRA_TOKEN)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # 📄 Format ADF (Atlassian Document Format)
    description_adf = {
        "version": 1,
        "type": "doc",
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": description_text
                    }
                ]
            }
        ]
    }

    payload = {
        "fields": {
            "project": {"key": PROJECT_KEY},
            "summary": summary,
            "issuetype": {"name": ISSUE_TYPE},
            "priority": {"name": priority},
            "description": description_adf  # 👈 Pakai ADF, bukan string biasa
        }
    }

    response = requests.post(
        url,
        data=json.dumps(payload),
        auth=auth,
        headers=headers
    )

    if response.status_code == 201:
        issue_key = response.json().get("key")
        print(f"✅ Task berhasil dibuat: {JIRA_URL}/browse/{issue_key}")
        return issue_key
    else:
        print(f"❌ Gagal buat task: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    create_jira_task(
        summary="High Risk Detected: Login Test",
        description_text="Login test memiliki probabilitas gagal 85% berdasarkan model AI. Disarankan segera diperiksa."
    )