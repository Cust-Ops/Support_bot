from atlassian import Jira
import re
from requests import HTTPError
from config import url_create, jira_c_api_token


def create_issue_tt(message, summary, nickname):
    jira = Jira(
        url=f'{url_create}',
        username='Keptcmeck@bk.ru',
        password=f'{jira_c_api_token}',
        cloud=True)

    issue_dict = {
        'project': {'id': '10002'},
        'issuetype': {"name": "Task"},
        "summary": f'{summary}',
        "description": f"{message}\nТелеграмм аккаунт для связи: @{nickname}.",
    }
    new_issue = jira.issue_create(issue_dict)
    issue_num = [new_issue[i] for i in sorted(new_issue.keys())]
    return issue_num[1]
    """os.unlink(src)"""


def status_of_issue(number):
    jira = Jira(
        url=f'{url_create}',
        username='Keptcmeck@bk.ru',
        password=f'{jira_c_api_token}',
        cloud=True)
    if re.match(r'[TtТт]+', f'{number.split("-")[0]}'):
        number = f'TT-{number.split("-")[1]}'
    if re.match(r'[ИиТт]+', f'{number.split("-")[0]}'):
        number = f'IT-{number.split("-")[1]}'
    try:
        req = f'{jira.issue(number)}'
        status = req.split("'iconUrl': 'https://cirex.atlassian.net/', 'name': '")[1].split("', 'id'", maxsplit=1)[0]
        author = req.split("'displayName': '")[1].split("', 'active'", maxsplit=1)[0]
        try:
            comment = req.split("Комментарий: ")[1].split("', 'updateAuthor': {")[0]
        except IndexError:
            comment = "Комментарий отсутсвует"
        if author == 'Телеграмм Бот':
            author = 'Работа по заявке еще не начата'
        return f'Заявка номер {number}, находиться в статусе "{status}"\nРаботу по заявке проводит: {author}\n' \
               f'Комментарий по запросу:\n{comment}'
    except HTTPError:
        return 'Заявки с этим номером не найдено, начните процесс получения статуса с начала'
