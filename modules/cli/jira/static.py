import os
from dotenv import load_dotenv


dotenv_path = os.path.realpath(os.path.join(os.path.dirname(__file__), "../../..", ".env"))

load_dotenv(dotenv_path)

_DOMAIN = "flcdata"
JIRA_DOMAIN = f"https://{_DOMAIN}.atlassian.net"
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_USER_ID = os.getenv("JIRA_USER_ID")


HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
