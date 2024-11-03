import mysql.connector

employee_count = 0
login_success = False
continue_process = True


def get_connection():
    return mysql.connector.connect(host='localhost', user='root', password='alpinePROJ_378', database='book_store')


def end_connection(cur, con):
    cur.close()
    con.close()


def create_table(table_name, columns):
    connector = get_connection()
    cursor = connector.cursor()

    columns_with_types = ", ".join(
        [f"{col} {data_type}" for col, data_type in columns.items()])
    query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types})"
    cursor.execute(query)
    cursor.close()
    connector.close()


# Creating the barebone of the database if it doesn't exist.
temporary_connector = mysql.connector.connect(
    host='localhost', user='root', password='alpinePROJ_378')
temp_cursor = temporary_connector.cursor()

temp_cursor.execute("CREATE DATABASE IF NOT EXISTS book_store")

create_table("login", {
    "username": "VARCHAR(15) PRIMARY KEY",
    "password": "VARCHAR(20)"
})

create_table("available_books", {
    "book_id": "VARCHAR(30) PRIMARY KEY",
    "book_title": "VARCHAR(80)",
    "genre": "VARCHAR(25)",
    "quantity": "INT",
    "author": "VARCHAR(50)",
    "publication": "VARCHAR(50)",
    "price": "FLOAT"
})

create_table("sale_record", {
    "customer_name": "VARCHAR(50) PRIMARY KEY",
    "phone_number": "INT",
    "book_title": "VARCHAR(80)",
    "quantity": "INT",
    "price": "FLOAT"
})

create_table("staff_details", {
    "staff_id": "INT PRIMARY KEY",
    "staff_name": "VARCHAR(50)",
    "gender": "CHAR(2)",
    "phone_number": "INT"
})

temp_cursor.execute('SELECT * FROM login')
result = temp_cursor.fetchall()
if result == None:
    temp_cursor.execute(
        "INSERT INTO login VALUES ('{}','{}')".format('book', 'store'))
    temporary_connector.commit()

end_connection(temp_cursor, temporary_connector)


def want_to_continue():
    global continue_process
    choice = input("\nDo you want to continue (y/n): ")

    if choice.lower() == 'y':
        continue_process = True
    elif choice.lower() == 'n':
        continue_process = False

# Admin Functions


def add_book():
    connector = get_connection()
    cursor = connector.cursor()

    id = input("\n    Book's ISBN: ")
    title = input("    Title: ")
    genre = input("    Genre: ")
    quantity = int(input("    Quantity: "))
    author = input("    Author: ")
    publication = input("    Publication: ")
    price = float(input("    Price: "))

    query = """
        INSERT INTO available_books (book_id, book_title, genre, quantity, author, publication, price)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (id, title, genre, quantity, author, publication, price)

    cursor.execute(query, values)
    connector.commit()
    print("\n    Book Added.")
    end_connection(cursor, connector)


def add_staff():
    global employee_count
    connector = get_connection()
    cursor = connector.cursor()

    staff_name = int(input("\n    Name: "))
    staff_id = employee_count + 1
    employee_count += 1
    gender = input("    Gender: ")
    phone_number = int(input("    Phone Number: "))

    query = "INSERT INTO staff_details VALUES ('{}','{}','{}','{}')".format(
        staff_name, staff_id, gender, phone_number)

    cursor.execute(query)
    connector.commit()
    print("\n    Staff hired.")
    end_connection(cursor, connector)


def remove_staff():
    connector = get_connection()
    cursor = connector.cursor()

    display_staff()

    id = int(input("\n    Enter Staff ID to remove: "))

    cursor.execute(
        "DELETE FROM staff_details WHERE staff_id = ('{}')".format(id))

    connector.commit()
    print("\n    Staff removed.")
    end_connection(cursor, connector)


def display_staff():
    connector = get_connection()
    cursor = connector.cursor()

    print()

    cursor.execute("SELECT * FROM staff_details")
    data = cursor.fetchall()

    for item in data:
        output = f'''
**********************************
    Employee ID: {item[0]}
    Name: {item[1]}
    Gender: {item[2]}
    Phone Number: {item[3]}
**********************************'''

        print(output)

    end_connection(cursor, connector)


def display_sale_record():
    connector = get_connection()
    cursor = connector.cursor()

    cursor.execute("SELECT * FROM sale_record")
    data = cursor.fetchall()

    for sale in data:
        print(f'''\n
        Buyer's Name: {sale[0]}
        Phone Number: {sale[1]}
        Book Title: {sale[2]}
        Quantity: {sale[1]}
        Price of 1 book: {sale[1]}
        ''')

    end_connection(cursor, connector)


def total_income():
    connector = get_connection()
    cursor = connector.cursor()

    cursor.execute("SELECT sum(price) FROM sale_record")
    data = cursor.fetchone()
    print(f"\n    Total Revenue: {data[0]}")
    end_connection(cursor, connector)


def display_stock():
    connector = get_connection()
    cursor = connector.cursor()

    cursor.execute("SELECT * FROM available_books ORDER BY book_title")
    data = cursor.fetchall()
    for item in data:
        output = f'''\n*******************************************************************
    Book ID: {item[0]}
    Book Title: {item[1]}
    Genre: {item[2]}
    Quantity: {item[3]}
    Author: {item[4]}
    Publication: {item[5]}
    Price: {item[6]}
*******************************************************************'''

        print(output)

    end_connection(cursor, connector)


def check_book_stock(book_name):
    connector = get_connection()
    cursor = connector.cursor()

    cursor.execute(
        "SELECT book_title FROM available_books WHERE book_name = {}".format(book_name))
    book = cursor.fetchone()
    exists = False
    available_quantity = 0
    price = 0

    if book[1] is not None:
        exists = True
        available_quantity = book[3]
        price = book[6]

    return exists, available_quantity, price

    end_connection(cursor, connector)


def search_books():
    connector = get_connection()
    cursor = connector.cursor()

    filtration = input('''
................................
    
    Options to search using:
    1. Name
    2. Genre
    3. Author
    4. Publication
                            
    Enter option: ''')

    if filtration.lower() == 'name':
        name_filter = input("Enter name to filter: ")
        cursor.execute("SELECT book_title FROM available_books")
        results = cursor.fetchall()

        for item in results:
            if name_filter.lower() in (item[1]).lower():
                output = f'''\n*******************************************************************
    Book ID: {item[0]}
    Book Title: {item[1]}
    Genre: {item[2]}
    Quantity: {item[3]}
    Author: {item[4]}
    Publication: {item[5]}
    Price: {item[6]}
*******************************************************************'''

                print(output)

    elif filtration.lower() == 'genre':
        genre_filter = input("Enter genre to filter: ")
        cursor.execute("SELECT genre FROM available_books")
        results = cursor.fetchall()

        for item in results:
            if genre_filter.lower() in (item[2]).lower():
                output = f'''\n*******************************************************************
    Book ID: {item[0]}
    Book Title: {item[1]}
    Genre: {item[2]}
    Quantity: {item[3]}
    Author: {item[4]}
    Publication: {item[5]}
    Price: {item[6]}
*******************************************************************'''

                print(output)

    elif filtration.lower() == 'author':
        author_filter = input("Enter author to filter: ")
        cursor.execute("SELECT author FROM available_books")
        results = cursor.fetchall()

        for item in results:
            if author_filter.lower() in (item[4]).lower():
                output = f'''\n*******************************************************************
    Book ID: {item[0]}
    Book Title: {item[1]}
    Genre: {item[2]}
    Quantity: {item[3]}
    Author: {item[4]}
    Publication: {item[5]}
    Price: {item[6]}
*******************************************************************'''

                print(output)

    elif filtration.lower() == 'publication':
        publication_filter = input("Enter publication to filter: ")
        cursor.execute("SELECT publication FROM available_books")
        results = cursor.fetchall()

        for item in results:
            if publication_filter.lower() in (item[5]).lower():
                output = f'''\n*******************************************************************
    Book ID: {item[0]}
    Book Title: {item[1]}
    Genre: {item[2]}
    Quantity: {item[3]}
    Author: {item[4]}
    Publication: {item[5]}
    Price: {item[6]}
*******************************************************************'''

                print(output)

    end_connection(cursor, connector)

# Customer specific Functions


def purchase():
    print("\nAvailable Books:")
    display_stock()

    customer_name = input("    Enter your name: ")
    phone_number = int(input("    Enter phone number: "))
    book = input("    Enter the book to purchase: ")
    quantity = int("    Enter the quantity to purchase: ")

    connector = get_connection()
    cursor = connector.cursor()

    stock_tuple = check_book_stock(book)

    if stock_tuple[0] == True:
        if stock_tuple[1] < quantity:
            print(f"Sorry, only {stock_tuple[1]} books are available.")
        else:
            cursor.execute("INSERT INTO sale_record VALUES ('{}','{}','{}','{}','{}')".format(
                customer_name, phone_number, book, quantity, stock_tuple[2]))

            cursor.execute(
                "UPDATE available_books SET quantity = {} WHERE book_name = {}".format((stock_tuple[1]-quantity), book))

            connector.commit()
            print("Transaction completed. Thank you.")
    else:
        print(f"Sorry, {book} is not available in our book store.")

    end_connection(cursor, connector)


# Main Program
option = input("""
      ALPINE BOOK STORE
.............................
            
    Options:
    1. Enter as ADMIN
    2. Enter as Customer
    
    Enter an option: """)

if option == '1':
    print("\n~~~~~~~~~LOGIN PAGE~~~~~~~~~")
    username = input("\n    Username: ")
    password = input("    Password: ")

    connector = get_connection()
    cursor = connector.cursor()

    cursor.execute(
        "SELECT * FROM login WHERE username = '{}'".format(username.strip()))
    data = cursor.fetchone()

    if data != None and data[1] == password.strip():
        login_success = True
    else:
        print("\n    Sorry, login failed. Incorrect credentials.")

    end_connection(cursor, connector)

    while continue_process and login_success:
        admin_choice = input('''
...............................
    
    Options:
    1. Add Books
    2. Manage Staff
    3. Display Sales
    4. Display Total Income
    5. See Available Books
    6. Search Books
                    
    Enter option: ''')

        if admin_choice == '1':
            add_book()
            want_to_continue()
        elif admin_choice == '2':
            manage_staff_choice = input("""
.............................
    
    Options:
    1. View Staff Details
    2. Hire Staff
    3. Fire Staff
                            
    Enter option: """)

            if manage_staff_choice == '1':
                display_staff()
                want_to_continue()
            elif manage_staff_choice == '2':
                add_staff()
                want_to_continue()
            elif manage_staff_choice == '3':
                display_staff()
                remove_staff()
                want_to_continue()
        elif admin_choice == '3':
            display_sale_record()
            want_to_continue()
        elif admin_choice == '4':
            total_income()
            want_to_continue()
        elif admin_choice == '5':
            display_stock()
            want_to_continue()
        elif admin_choice == '6':
            search_books()
            want_to_continue()
        else:
            break
elif option == '2':
    while continue_process:
        buyer_choice = input('''
...............................
    
    Options:
    1. See all available books
    2. Search books
    3. Purchase Books
                    
    Enter option: ''')

        if buyer_choice == '1':
            display_stock()
            want_to_continue()
        elif buyer_choice == '2':
            search_books()
            want_to_continue()
        elif buyer_choice == '3':
            purchase()
            want_to_continue()
        else:
            break
