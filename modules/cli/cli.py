import sys
from .jira.issue import Issue


def cli(args=None):
    """ Process command line arguments. """
    if not args:
        args = sys.argv[1:]
        domain = args[0]
        if domain == "jira":
            return Issue().get_issue_description(*args[1:])


def cli_output(message):
    return sys.stdout.write(message)
