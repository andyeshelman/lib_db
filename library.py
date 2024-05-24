from myconn import handy, make_conn

MAX_BORROWED = 10

@handy
def add_user(name, email):
    with make_conn() as conn, conn.cursor() as cursor:
        query = "INSERT INTO Users(name, email) VALUES (%s, %s)"
        cursor.execute(query, (name, email))
        conn.commit()
        return 201

@handy
def add_book(title, author, pub_year):
    with make_conn() as conn, conn.cursor() as cursor:
        query = "INSERT INTO Media(title) VALUES (%s)"
        cursor.execute(query, (title,))
        conn.commit()
        book_id = cursor.lastrowid
        query = "INSERT INTO Books(book_id, author, pub_year) VALUES (%s, %s, %s)"
        cursor.execute(query, (book_id, author, pub_year))
        conn.commit()
        return 201

@handy
def add_movie(title, director, rel_year):
    with make_conn() as conn, conn.cursor() as cursor:
        query = "INSERT INTO Media(title) VALUES (%s)"
        cursor.execute(query, (title,))
        conn.commit()
        movie_id = cursor.lastrowid
        query = "INSERT INTO Movies(movie_id, director, rel_year) VALUES (%s, %s, %s)"
        cursor.execute(query, (movie_id, director, rel_year))
        conn.commit()
        return 201

@handy
def get_users():
    with make_conn() as conn, conn.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM Users")
        return cursor.fetchall()

@handy
def get_user(user_id):
    with make_conn() as conn, conn.cursor(dictionary=True) as cursor:
        cursor.execute(f"SELECT * FROM Users WHERE user_id = {user_id}")
        return cursor.fetchone()

@handy
def get_media(media_id):
    with make_conn() as conn, conn.cursor(dictionary=True) as cursor:
        cursor.execute(f"SELECT * FROM Media WHERE media_id = {media_id}")
        media = cursor.fetchone()
        if not media:
            return None
        cursor.execute(f"SELECT * FROM Books WHERE book_id = {media_id}")
        book = cursor.fetchone()
        if book:
            return book | media
        cursor.execute(f"SELECT * FROM Movies WHERE movie_id = {media_id}")
        return cursor.fetchone() | media

@handy
def get_borrowed_by_user(user_id):
    with make_conn() as conn, conn.cursor(dictionary=True) as cursor:
        cursor.execute(f"SELECT * FROM Borrowed WHERE user_id = {user_id}")
        return (get_media(media["media_id"]) for media in cursor.fetchall())

@handy
def get_collection():
    with make_conn() as conn, conn.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM Media")
        return (get_media(media["media_id"]) for media in cursor.fetchall())

@handy
def in_collection(media_id):
    with make_conn() as conn, conn.cursor(dictionary=True) as cursor:
        cursor.execute(f"SELECT * FROM Media WHERE media_id = {media_id}")
        return cursor.fetchone()

@handy
def get_borrowed(media_id):
    with make_conn() as conn, conn.cursor(dictionary=True) as cursor:
        cursor.execute(f"SELECT * FROM Borrowed WHERE media_id = {media_id}")
        return cursor.fetchone()

@handy
def checkout(user_id, media_id):
    if not in_collection(media_id):
        return "no media"
    if not get_user(user_id):
        return "no user"
    borrowed = get_borrowed_by_user(user_id)
    if len(list(borrowed)) >= MAX_BORROWED:
        return "max"
    if any(media_id == media["media_id"] for media in borrowed):
        return "dup"
    if get_borrowed(media_id):
        return "out"
    with make_conn() as conn, conn.cursor(dictionary=True) as cursor:
        query = "INSERT INTO Borrowed(user_id, media_id) VALUES (%s, %s)"
        cursor.execute(query, (user_id, media_id))
        conn.commit()
        return 201

@handy
def checkin(media_id, user_id = None):
    if user_id is None:
        if not get_borrowed(media_id):
            return "not checked"
        with make_conn() as conn, conn.cursor(dictionary=True) as cursor:
            cursor.execute(f"DELETE FROM Borrowed WHERE media_id = {media_id}")
            conn.commit()
            return 200
    if not in_collection(media_id):
        return "no media"
    borrowed = get_borrowed(media_id)
    if not borrowed or user_id != borrowed["user_id"]:
        return "not checked"
    with make_conn() as conn, conn.cursor(dictionary=True) as cursor:
        cursor.execute(f"DELETE FROM Borrowed WHERE media_id = {media_id}")
        conn.commit()
        return 200