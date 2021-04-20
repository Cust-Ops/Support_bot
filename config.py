from atlassian import Jira
from datetime import date

token_bot = '1721490273:AAFfuOmgC_nQWmhaLTyKmsND11EjMWwCNTc'
chat_id = '-1001245632429'
url_create = 'https://cirex.atlassian.net/'
jira_t_api_token = 'aCwkZaqDQlKIwbNxqUdR5D67'
jira_c_api_token = '1Ka7FVtPJBtnzuxBcykJBF01'
request_type = int
deadline = date.today()


def create_issue(message, summary, nickname):
    jira = Jira(
        url=f'{url_create}',
        username='Keptcmeck@bk.ru',
        password=f'{jira_c_api_token}',
        cloud=True)

    jira.issue_create(fields={
        'project': {'id': '10002'},
        'issuetype': {"name": "Task"},
        "summary": f'{summary}',
        "description": f"{message}\nТелеграмм аккаунт для связи: @{nickname}",
    })


