from config import config
import psycopg2 as pg2


def connect_db():
    try:
        params = config()
        connection = pg2.connect(**params)
        db_cursor = connection.cursor()
        qr = 'SELECT version()'
        db_cursor.execute(qr)
        print(db_cursor.fetchone())
        db_cursor.close()
    except (Exception, pg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()


if __name__ == '__main__':
    connect_db()
