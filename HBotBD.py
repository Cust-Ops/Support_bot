import psycopg2
from config import postgre_user, postgre_pass

con = psycopg2.connect(
  database="telebot",
  user=postgre_user,
  password=postgre_pass,
  host="localhost",
  port="5432"
)
print('Database opened successfully')


def create_new_user(chatid, username, fname, sname):  # Создание новой строчки в таблице UsersBD
    print(f'Trying to create new record with value: {chatid, username, fname, sname}')
    cur = con.cursor()
    cur.execute("SELECT chatid FROM usersdb")
    rows = cur.fetchall()
    for row in rows:
        if chatid == row[0]:
            return print('This user is already in the database')
    cur.execute(
        f"INSERT INTO usersdb (ID,CHATID,USERNAME,FNAME,SNAME,ACTIVE,COMPANY) "
        f"VALUES (DEFAULT, {chatid}, '@{username}', '{fname}', '{sname}', true, 'insert here')"
    )
    con.commit()
    print("Record inserted successfully")


def create_new_issue(chatid, typer, doc, text, request):  # Создарние новой строчки в таблице IssueBD
    print(f'Creating new record in table requestsbd with value: {chatid}, {typer}, {doc}, {text}')
    cur = con.cursor()
    cur.execute(
        f"INSERT INTO requestsbd (ID, CHATID, TYPE, DOC,  BODY, CREATE_DATE, JIRA_LINK) "
        f"VALUES (DEFAULT, {chatid}, '{typer}', {doc}, '{text}', CURRENT_TIMESTAMP(0), '{request}')"
    )
    con.commit()
    print('Record inserted successfully')
