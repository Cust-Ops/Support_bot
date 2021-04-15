from atlassian import Jira

token_bot = '1721490273:AAFfuOmgC_nQWmhaLTyKmsND11EjMWwCNTc'
chat_id = '-1001255614977'
url_create = 'https://cirex.atlassian.net/'
jira_t_api_token = 'aCwkZaqDQlKIwbNxqUdR5D67'
jira_c_api_token = '1Ka7FVtPJBtnzuxBcykJBF01'
request_type = int


def create_issue(message, summary, nickname):
    jira = Jira(
        url=f'{url_create}',
        username='Keptcmeck@bk.ru',
        password=f'{jira_c_api_token}',
        cloud=True)

    jira.issue_create(fields={
        'project': {'id': '10000'},
        'issuetype': {
            "name": "Task"
        },
         'summary': f'{summary}',
         'description': f"{message}\nТелеграмм аккаунт для связи: @{nickname}",
    })
