jira-issue:
	poetry run cli jira $(ISSUE)

lint:
	poetry run flake8

check-integration:
	docker-compose up --build
