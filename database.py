import sqlite3


db = sqlite3.connect('MuseMatrix_tg.db')
cur = db.cursor()


async def db_start():
    cur.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, telegram_id INT UNIQUE, auth_token VARCHAR(255))')


async def db_create(tg_id):
    user = cur.execute('SELECT telegram_id FROM users WHERE telegram_id == {tg_id}'.format(tg_id=tg_id)).fetchone()
    if not user:
        cur.execute('INSERT INTO users (telegram_id) VALUES ({tg_id})'.format(tg_id=tg_id))
        db.commit()


async def db_update(tg_id, auth_token):
    cur.execute('UPDATE users SET auth_token = "{auth_token}" WHERE telegram_id == {tg_id}'.format(auth_token=auth_token, tg_id=tg_id))
    db.commit()


async def db_read(tg_id):
    auth_token = cur.execute('SELECT auth_token FROM users WHERE telegram_id == {tg_id}'.format(tg_id=tg_id)).fetchone()
    return auth_token[0]