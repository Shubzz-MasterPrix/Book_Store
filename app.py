import mysql.connector
import getpass

employee_count = 0
login_success = False
continue_process = True


def get_connection():
    return mysql.connector.connect(host='localhost', user='root', password='', database='book_store')


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
    host='localhost', user='root', password='')
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
    "revenue": "FLOAT"
})

create_table("staff_details", {
    "staff_id": "INT PRIMARY KEY",
    "staff_name": "VARCHAR(50)",
    "gender": "CHAR(2)",
    "phone_number": "INT"
})

temporary_connector = mysql.connector.connect(
    host='localhost', user='root', password='', database='book_store')
temp_cursor = temporary_connector.cursor()

temp_cursor.execute('SELECT * FROM login')
result = temp_cursor.fetchall()
if not result:
    temp_cursor.execute(
        "INSERT INTO login VALUES ('{}','{}')".format('book', 'store'))
    temporary_connector.commit()

end_connection(temp_cursor, temporary_connector)


def want_to_continue():
    global continue_process

    while True:
        choice = input("\n    Do you want to continue (y/n): ")

        if choice.lower() == 'y':
            continue_process = True
            break
        elif choice.lower() == 'n':
            continue_process = False
            break
        else:
            print("\n    Invalid choice, try again.")

# Admin Functions


def add_book():
    connector = get_connection()
    cursor = connector.cursor()

    id = input("\n    Book's ISBN: ")
    title = input("    Title: ")
    genre = input('''    List of genres:
    -> Fiction
    -> Non-Fiction
    -> Mystery & Thriller
    -> Fantasy
    -> Science Fiction
    -> Romance
    -> Historical Fiction
    -> Biography & Memoir
    -> Self-Help
    -> Graphic Novels & Comics
    -> Poetry
    -> Children's
    -> Classic Literature
    -> Science & Technology
    -> Health & Wellness
    -> Cookbooks
    -> Art & Photography
    -> Spirituality & Religion
    -> Crime     
    
    Genre: ''')
    quantity = int(input("    Quantity: "))
    author = input("    Author: ")
    publication = input("    Publication: ")
    price = float(input("    Price: ₹"))

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

    staff_name = input("\n    Name: ")
    staff_id = employee_count + 1
    employee_count += 1
    gender = input("    Gender (M/F): ")
    phone_number = int(input("    Phone Number: "))

    query = "INSERT INTO staff_details VALUES ({},'{}','{}',{})".format(
        staff_id, staff_name, gender, phone_number)

    cursor.execute(query)
    connector.commit()
    print("\n    Staff hired.")
    end_connection(cursor, connector)


def remove_staff():
    connector = get_connection()
    cursor = connector.cursor()

    display_staff()

    if employee_count != 0:
        id = int(input("\n    Enter Staff ID number to remove: "))

    cursor.execute(
        "DELETE FROM staff_details WHERE staff_id = ({})".format(id))

    connector.commit()
    print("\n    Staff removed.")
    end_connection(cursor, connector)


def display_staff():
    connector = get_connection()
    cursor = connector.cursor()

    print()

    cursor.execute("SELECT * FROM staff_details")
    data = cursor.fetchall()

    if not data:
        print("    No staff currently.")
    else:
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

    if not data:
        print("\n    No sales so far.")

    else:
        for sale in data:
            print(f'''\n
    Buyer's Name: {sale[0]}
    Phone Number: {sale[1]}
    Book Title: {sale[2]}
    Quantity: {sale[3]}
    Price: ₹{sale[4]}
    ''')

    end_connection(cursor, connector)


def total_income():
    connector = get_connection()
    cursor = connector.cursor()

    cursor.execute("SELECT sum(price) FROM sale_record")
    data = cursor.fetchone()

    if data[0] != None:
        print(f"\n    Total Revenue: ₹{round(data[0], 2)}")
    else:
        print("\n    Total Revenue: ₹0")
    end_connection(cursor, connector)


def display_stock():
    connector = get_connection()
    cursor = connector.cursor()

    cursor.execute("SELECT * FROM available_books ORDER BY book_title")
    data = cursor.fetchall()

    if not data:
        print("No stock available.")
    else:
        for item in data:
            output = f'''\n*******************************************************************
    Book ID: {item[0]}
    Book Title: {item[1]}
    Genre: {item[2]}
    Quantity: {item[3]}
    Author: {item[4]}
    Publication: {item[5]}
    Price: ₹{item[6]}
*******************************************************************'''

            print(output)

    end_connection(cursor, connector)


def search_books():
    connector = get_connection()
    cursor = connector.cursor()

    while True:
        filtration = input('''
................................
    
    Options to search using:
    1. Title
    2. Genre
    3. Author
    4. Publication
                            
    Enter option (1/2/3/4): ''')

        cursor.execute("SELECT * FROM available_books")
        results = cursor.fetchall()
        found = False

        if filtration == '1':
            name_filter = input("    Enter name to filter: ")

            for item in results:
                if name_filter.lower() in (item[1]).lower():
                    found = True
                    print(f'''\n*******************************************************************
    Book ID: {item[0]}
    Book Title: {item[1]}
    Genre: {item[2]}
    Quantity: {item[3]}
    Author: {item[4]}
    Publication: {item[5]}
    Price: ₹{item[6]}
*******************************************************************''')
            if found == False:
                print("Sorry, no such books were found.")
            break

        elif filtration == '2':
            genre_filter = input('''    
    List of genres:
    -> Fiction
    -> Non-Fiction
    -> Mystery & Thriller
    -> Fantasy
    -> Science Fiction
    -> Romance
    -> Historical Fiction
    -> Biography & Memoir
    -> Self-Help
    -> Graphic Novels & Comics
    -> Poetry
    -> Children's
    -> Classic Literature
    -> Science & Technology
    -> Health & Wellness
    -> Cookbooks
    -> Art & Photography
    -> Spirituality & Religion
    -> Crime     
    
    Enter genre to filter: ''')

            for item in results:
                if genre_filter.lower().strip() in (item[2]).lower().strip():
                    found = True
                    print(f'''\n*******************************************************************
    Book ID: {item[0]}
    Book Title: {item[1]}
    Genre: {item[2]}
    Quantity: {item[3]}
    Author: {item[4]}
    Publication: {item[5]}
    Price: ₹{item[6]}
*******************************************************************''')

            if found == False:
                print("Sorry, no such books were found.")
            break

        elif filtration == '3':
            author_filter = input("    Enter author to filter: ")

            for item in results:
                if author_filter.lower() in (item[4]).lower():
                    found = True
                    print(f'''\n*******************************************************************
    Book ID: {item[0]}
    Book Title: {item[1]}
    Genre: {item[2]}
    Quantity: {item[3]}
    Author: {item[4]}
    Publication: {item[5]}
    Price: ₹{item[6]}
*******************************************************************''')
            if found == False:
                print("Sorry, no such books were found.")
            break

        elif filtration == '4':
            publication_filter = input("    Enter publication to filter: ")

            for item in results:
                if publication_filter.lower() in (item[5]).lower():
                    found = True
                    print(f'''\n*******************************************************************
    Book ID: {item[0]}
    Book Title: {item[1]}
    Genre: {item[2]}
    Quantity: {item[3]}
    Author: {item[4]}
    Publication: {item[5]}
    Price: ₹{item[6]}
*******************************************************************''')
            if found == False:
                print("Sorry, no such books were found.")
            break

        else:
            print("\n    Invalid option, try again.")
    end_connection(cursor, connector)

# Customer specific Functions


def purchase():
    customer_name = input("    Enter your name: ")
    phone_number = int(input("    Enter phone number: "))
    book = input("    Enter the title of the book to purchase: ")
    quantity = int(input("    Enter the quantity to purchase: "))

    connector = get_connection()
    cursor = connector.cursor()

    cursor.execute(
        "SELECT * FROM available_books WHERE book_title = %s", (book,))
    result = cursor.fetchone()

    if result != None:
        available_quantity = result[3]

        if quantity < 1:
            print("Sorry, please enter a value greater than 0.")
        elif available_quantity < quantity:
            print(f"Sorry, only {available_quantity} pieces of the book are available.")  # noqa
        else:
            cursor.execute("INSERT INTO sale_record (customer_name, phone_number, book_title, quantity, price) VALUES (%s,%s,%s,%s,%s)",
                           (customer_name, phone_number, book, quantity, (result[6]*quantity)))

            cursor.execute(
                "UPDATE available_books SET quantity = %s WHERE book_title = %s", ((available_quantity-quantity), book))

            connector.commit()
            print("\n    Transaction completed. Thank you.")
    else:
        print(f"Sorry, {book} is not available in our book store.")

    end_connection(cursor, connector)


# Main Program
option = input("""
         BOOK STORE
.............................
            
    Options:
    1. Enter as ADMIN
    2. Enter as Customer
    3. Exit
    
    Enter an option: """)

while continue_process:
    if option == '1':
        print("\n~~~~~~~~~LOGIN PAGE~~~~~~~~~")
        username = input("\n    Username: ")
        password = getpass.getpass("    Password (hidden while typing): ")

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
    7. Exit
                    
    Enter option: ''')

            if admin_choice == '1':
                add_book()
                want_to_continue()
            elif admin_choice == '2':
                while True:

                    manage_staff_choice = input("""
.............................
    
    Options:
    1. View Staff Details
    2. Hire Staff
    3. Fire Staff
    4. Exit this menu
                            
    Enter option: """)

                    if manage_staff_choice == '1':
                        display_staff()
                        want_to_continue()
                        break
                    elif manage_staff_choice == '2':
                        add_staff()
                        want_to_continue()
                        break
                    elif manage_staff_choice == '3':
                        display_staff()
                        remove_staff()
                        want_to_continue()
                        break
                    elif manage_staff_choice == '4':
                        break
                    else:
                        print("\n    Invalid option, try again.")
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
            elif admin_choice == '7':
                continue_process = False
            else:
                print("\n    Invalid option, try again.")
    elif option == '2':
        while continue_process:
            buyer_choice = input('''
...............................
    
    Options:
    1. See all available books
    2. Search books
    3. Purchase Books
    4. Exit
                    
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
            elif buyer_choice == '4':
                continue_process = False
            else:
                print("\n    Invalid option, try again.")
    elif option == '3':
        continue_process = False
    else:
        print("\n    Invalid option, try again.")
        option = input("    Enter option: ")
