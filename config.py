from atlassian import Jira as ajira
import os


token_bot_main = '1721490273:AAFfuOmgC_nQWmhaLTyKmsND11EjMWwCNTc'
token_bot_test = '1531195994:AAFT5mSp3GZ_38vHz76-9M1UQ6Xh6Fae6fI'
chat_id = '-1001245632429'
chat_test_id = '-1001472777670'
url_create = 'https://cirex.atlassian.net/'
jira_c_api_token = '1Ka7FVtPJBtnzuxBcykJBF01'
request_type = int


def create_issue_tty(message, summary, nickname):
    ttnjira = ajira(
        url=f'{url_create}',
        username='Keptcmeck@bk.ru',
        password=f'{jira_c_api_token}',
        cloud=True)

    ttnjira.issue_create(fields={
        'project': {'id': '10002'},
        'issuetype': {"name": "Task"},
        "summary": f'{summary}',
        "description": f"{message}\nТелеграмм аккаунт для связи: @{nickname}.",
    })
    """os.unlink(src)"""


def create_issue_ttn(message, summary, nickname):
    ttyjira = ajira(
        url=f'{url_create}',
        username='Keptcmeck@bk.ru',
        password=f'{jira_c_api_token}',
        cloud=True)

    ttyjira.issue_create(fields={
        'project': {'id': '10002'},
        'issuetype': {"name": "Task"},
        "summary": f'{summary}',
        "description": f"{message}\nТелеграмм аккаунт для связи: @{nickname}",
    })
