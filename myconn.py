import mysql.connector

from config import HOST, USER, PASSWORD, DATABASE

def handy(func):
    def handy_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except mysql.connector.Error as e:
            print(f"ERROR in {func.__name__}: {e}")
            return None
    return handy_func

@handy
def make_conn():
    conn = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE,
    )
    if conn.is_connected():
        return conn
    print("No connection")
    return None