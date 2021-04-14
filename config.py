import sqlite3 as sql # БД

token_bot = '1721490273:AAFfuOmgC_nQWmhaLTyKmsND11EjMWwCNTc'
chat_id = '-1001255614977'


"""def generator_id(last_id):
    if len(last_id) == 0:
        last_id = 0
        new_id = last_id + 1
    else:
        new_id = last_id[-1] + 1
    return new_id"""


"""def sql_work(choice, name, surname, type_request, message):
    con = sql.connect('HelpBot.db')
    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS `HelpBot` ('id' INTEGER,`name` STRING, `surname` STRING, "
                    "'type' STRING, 'message' STRING)")
        cur.execute("SELECT id FROM 'HelpBot'")
        last_id = cur.fetchall()
        generator_id(last_id)
    with con:
        cur = con.cursor()
        if choice == 1:
            cur.execute(f"INSERT INTO `HelpBot` VALUES ('{last_id}', '{name}', '{surname}', '{type_request}', "
                        f"'{message}')")
        elif choice == 2:
            cur.execute("SELECT * FROM `HelpBot`")
            rows = cur.fetchall()
            for row in rows:
                print(row[0], row[1])
        else:
            print("Вы ошиблись")

        con.commit()
        cur.close()"""


# sql_work(1, 'Alex', 'Bovin', '123', '123')
