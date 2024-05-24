import re

import library

def valid_email(email):
    return bool(re.match(r"^\w[\+\.\w-]*@([\w-]+\.)*\w+[\w-]*\.([a-z]{2,4}|\d+)$", email))

def display_user(user):
    print(f"--- User {user["user_id"]} ---")
    print(f"\tName: {user["name"]}")
    print(f"\tEmail: {user["email"]}")

def display_media(media):
    if "book_id" in media:
        print(f"--- Book {media["book_id"]} ---")
        print(f"\tTitle: {media["title"]}")
        print(f"\tAuthor: {media["author"]}")
        print(f"\tPublication Year: {media["pub_year"]}")
    elif "movie_id" in media:
        print(f"--- Movie {media["movie_id"]} ---")
        print(f"\tTitle: {media["title"]}")
        print(f"\tDirector: {media["director"]}")
        print(f"\tRelease Year: {media["rel_year"]}")

def user_menu(user_id):
    while True:
        command = input(f"[User {user_id}] view, checkout, return, back>").strip().lower()
       
        if command == "view":
            cmnd = input(f"[User {user_id}:View] info, borrowed>")
            if cmnd == "info":
                display_user(library.get_user(user_id))
            elif cmnd == "borrowed":
                borrowed = library.get_borrowed_by_user(user_id)
                for media in borrowed:
                    display_media(media)
       
        elif command == "checkout":
            media_id = input(f"[User {user_id}:Checkout] Media ID>").strip()
            if not media_id.isdigit():
                print("Media ID must be an integer...")
                continue
            media_id = int(media_id)
            result = library.checkout(user_id, media_id)
            if result == 201:
                print("Checkout successful!")
            elif result == "max":
                print("User is maxed out. Return stuff to check more out...")
            elif result == "dup":
                print("User already has item checked out...")
            elif result == "out":
                print("Item unavailable.")
            elif result == "no media":
                print("Media unfound...")
        
        elif command == "return":
            media_id = input(f"[User {user_id}:Return] Media ID>")
            if not media_id.isdigit():
                print("Media ID must be an integer...")
                continue
            media_id = int(media_id)
            result = library.checkin(media_id, user_id)
            if result == 200:
                print("Return successful!")
            elif result == "no media":
                print("Media unfound...")
            elif result == "not checked":
                print("User is not currently borrowing this item...")
       
        elif command == "back":
            break
        
        else:
            print("Command unrecognized...")

def users_menu():
    while True:
        command = input("[Users] add, view, select, back>").strip().lower()
       
        if command == "add":
            name = input("Enter name: ").strip()
            if len(name) > 255:
                print("Name is too long...")
                continue
            email = input("Enter email: ").strip()
            if not valid_email(email):
                print("Invalid email...")
                continue
            library.add_user(name, email)
       
        elif command == "view":
            for user in library.get_users():
                display_user(user)
        
        elif command == "select":
            user_id = input("[Users] User ID>").strip()
            if not user_id.isdigit:
                print("User ID must be an integer...")
                continue
            user_id = int(user_id)
            if library.get_user(user_id):
                user_menu(user_id)
            else:
                print("User unfound...")
       
        elif command == "back":
            break
        
        else:
            print("Command unrecognized...")

def media_menu(media_id):
    while True:
        command = input(f"[Item {media_id}] view, checkout, return, back>").strip().lower()
        
        if command == "view":
            display_media(library.get_media(media_id))
        
        elif command == "checkout":
            user_id = input(f"[Item {media_id}:Checkout] User ID>")
            if not user_id.isdigit():
                print("User ID must be an integer...")
                continue
            user_id = int(user_id)
            result = library.checkout(user_id, media_id)
            if result == 201:
                print("Checkout successful!")
            elif result == "max":
                print("User is maxed out. Return stuff or drop holds to check more out...")
            elif result == "dup":
                print("User already has item checked out...")
            elif result == "out":
                print("Item unavailable.")
            elif result == "no user":
                print("User unfound...")
        
        elif command == "return":
            result = library.checkin(media_id)
            if result == "not checked":
                print("Item is not checked out")
            elif result == 200:
                print("Return successful!")
        
        elif command == "back":
            break
        
        else:
            print("Command unrecognized...")

def collection_menu():
    while True:
        command = input("[Collection] add, view, select, back>").strip().lower()
        
        if command == "add":
            medium = input("[Medium] book, movie>").strip().lower()
            if medium == "book":
                title = input("Enter title: ")
                if len(title) > 255:
                    print("Title is too long...")
                    continue
                author = input("Enter author: ")
                if len(author) > 255:
                    print("Author is too long...")
                    continue
                pub_year = input("Enter publication year: ")
                if not pub_year.isdigit() or not len(pub_year) == 4:
                    print("Year must be in YYYY format")
                    continue
                if pub_year < "1901" or pub_year > "2155":
                    print("Publication year must fall between 1901 and 2155....")
                    continue
                library.add_book(title, author, pub_year)
                print("Book added successfully!")
            elif medium == "movie":
                title = input("Enter title: ")
                if len(title) > 255:
                    print("Title is too long...")
                    continue
                director = input("Enter director: ")
                if len(director) > 255:
                    print("Director is too long...")
                    continue
                rel_year = input("Enter release year: ")
                if not rel_year.isdigit() or not len(rel_year) == 4:
                    print("Year must be in YYYY format")
                    continue
                if rel_year < "1901" or rel_year > "2155":
                    print("Release year must fall between 1901 and 2155....")
                    continue
                library.add_movie(title, director, rel_year)
                print("Movie added successfully!")
            else:
                print("Medium unsupported...")
        
        elif command == "view":
            for media in library.get_collection():
                display_media(media)
        
        elif command == "select":
            media_id = input("[Collection] Media ID>").strip()
            if not media_id.isdigit():
                print("Media ID must be an integer...")
                continue
            media_id = int(media_id)
            if library.get_media(media_id):
                media_menu(media_id)
            else:
                print("Media unfound...")
        
        elif command == "back":
            break
        
        else:
            print("Command unrecognized...")

def main():
    while True:
        command = input("[Main Menu] users, collection, quit>").strip().lower() 
        if command == "users":
            users_menu()
        elif command == "collection":
            collection_menu()
        elif command == "quit":
            break
        else:
            print("Command unrecognized...")

main()