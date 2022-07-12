""" Get Jira Issue Description by id """
from jira import JIRA
from . import static
from .. import cli


class Issue:
    def __init__(self) -> None:
        self.JIRA_USER_ID = static.JIRA_USER_ID
        self.JIRA_API_TOKEN = static.JIRA_API_TOKEN
        self.JIRA_DOMAIN = static.JIRA_DOMAIN
        self._jira_client()

    def _jira_client(self):
        self.JIRA_CLIENT = JIRA(server=self.JIRA_DOMAIN, basic_auth=(self.JIRA_USER_ID, self.JIRA_API_TOKEN))

    def get_issue_description(self, issue_id: str) -> str:
        """
        Extracts the issue description on the jira board.

        Args:
            issue_id: str: Jira Issue Id.

        Returns:
            A string describing the task on the jira board.
        """

        issue = self.JIRA_CLIENT.issue(issue_id)
        issue_description = issue.fields.description
        if issue_description is None:
            issue_description = "Issue without a Jira's description"
        return cli.cli_output(issue_description)
