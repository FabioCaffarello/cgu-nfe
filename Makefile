jira-issue:
	poetry run cli jira $(ISSUE)

lint:
	poetry run flake8
