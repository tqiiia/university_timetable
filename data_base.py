import sqlite3 as sq


# noinspection PyGlobalUndefined
async def db_start():
    global db, cur
    db = sq.connect('students.db')
    cur = db.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS profile(id TEXT PRIMARY KEY, Группа TEXT, Оповещения TEXT)")

    db.commit()


async def create_profile(user_id):
    user = cur.execute("SELECT 1 FROM profile WHERE id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO profile VALUES(?, ?, ?)",
                    (user_id, '', ''))
        db.commit()
    else:
        user_data = cur.execute("SELECT * FROM profile WHERE id == '{key}'".format(key=user_id)).fetchone()
        group = user_data[1]
        print(group)
        db.commit()
        return group


# async def user_group(user_id):
#     user_data = cur.execute("SELECT * FROM profile WHERE id == '{key}'".format(key=user_id)).fetchone()
#     if user_data:
#         group = user_data[1]
#         print(group)
#         db.commit()
#         return group


async def edit_profile(state, user_id):
    async with state.proxy() as data:
        cur.execute("""UPDATE profile SET 
                        Группа = '{}'

                        WHERE id == '{}'""".format
                    (data['group'], user_id))
        db.commit()
