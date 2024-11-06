from flask_cors import CORS
from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)
CORS(app)
def get_connection():
    return mysql.connector.connect(host='localhost', user='root', password='Password!', database='book_store')

@app.route('/api/books', methods=['POST'])
def add_book():
    data = request.json
    try:
        connector = get_connection()
        cursor = connector.cursor()
	 
        query = "INSERT INTO available_books (book_id, book_title, genre, quantity, author, publication, price)  VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (data['id'], data['title'], data['genre'], data['quantity'], data['author'], data['publication'], data['price'])
       

        cursor.execute(query, values)
        connector.commit()
        return jsonify({"message": "Book added successfully."}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    finally:
        cursor.close()
        connector.close()

@app.route('/api/books', methods=['GET'])
def get_books():
    try:
        connector = get_connection()
        cursor = connector.cursor()
        
        cursor.execute("SELECT * FROM available_books")
        books = cursor.fetchall()
        
        book_list = []
        for book in books:
            book_list.append({
                "book_id": book[0],
                "title": book[1],
                "genre": book[2],
                "quantity": book[3],
                "author": book[4],
                "publication": book[5],
                "price": book[6]
            })
        return jsonify(book_list), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    finally:
        cursor.close()
        connector.close()

@app.route('/api/books/<book_id>', methods=['DELETE'])
def remove_book(book_id):
    try:
        connector = get_connection()
        cursor = connector.cursor()

        cursor.execute("DELETE FROM available_books WHERE book_id = %s", (book_id,))
        connector.commit()
        
        return jsonify({"message": "Book removed successfully."}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    finally:
        cursor.close()
        connector.close()

@app.route('/api/staff', methods=['POST'])
def add_staff():
    data = request.json
    try:
        connector = get_connection()
        cursor = connector.cursor()

        query = "INSERT INTO staff_details (staff_id, staff_name, gender, phone_number) VALUES (%s, %s, %s, %s)"
        staff_id = get_next_staff_id()  # Function to get the next available staff ID
        values = (staff_id, data['name'], data['gender'], data['phone_number'])
        
        cursor.execute(query, values)
        connector.commit()
        return jsonify({"message": "Staff member added successfully."}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    finally:
        cursor.close()
        connector.close()

def get_next_staff_id():
    connector = get_connection()
    cursor = connector.cursor()
    cursor.execute("SELECT MAX(staff_id) FROM staff_details")
    result = cursor.fetchone()
    cursor.close()
    connector.close()
    return (result[0] or 0) + 1

@app.route('/api/staff', methods=['GET'])
def get_staff():
    try:
        connector = get_connection()
        cursor = connector.cursor()
        
        cursor.execute("SELECT * FROM staff_details")
        staff = cursor.fetchall()
        
        staff_list = []
        for member in staff:
            staff_list.append({
                "staff_id": member[0],
                "name": member[1],
                "gender": member[2],
                "phone_number": member[3]
            })
        return jsonify(staff_list), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    finally:
        cursor.close()
        connector.close()

@app.route('/api/staff/<int:staff_id>', methods=['DELETE'])
def remove_staff(staff_id):
    try:
        connector = get_connection()
        cursor = connector.cursor()

        cursor.execute("DELETE FROM staff_details WHERE staff_id = %s", (staff_id,))
        connector.commit()
        
        return jsonify({"message": "Staff member removed successfully."}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    finally:
        cursor.close()
        connector.close()

@app.route('/api/sales', methods=['POST'])
def record_sale():
    data = request.json
    try:
        connector = get_connection()
        cursor = connector.cursor()

        query = """
            INSERT INTO sale_record (customer_name, phone_number, book_title, quantity, revenue)
            VALUES (%s, %s, %s, %s, %s)
        """
        revenue = data['price'] * data['quantity']
        values = (data['customer_name'], data['phone_number'], data['book_title'], data['quantity'], revenue)
        
        cursor.execute(query, values)
        connector.commit()
        return jsonify({"message": "Sale recorded successfully."}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    finally:
        cursor.close()
        connector.close()

@app.route('/api/sales', methods=['GET'])
def get_sales():
    try:
        connector = get_connection()
        cursor = connector.cursor()
        
        cursor.execute("SELECT * FROM sale_record")
        sales = cursor.fetchall()
        
        sale_list = []
        for sale in sales:
            sale_list.append({
                "customer_name": sale[0],
                "phone_number": sale[1],
                "book_title": sale[2],
                "quantity": sale[3],
                "revenue": sale[4]
            })
        return jsonify(sale_list), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    finally:
        cursor.close()
        connector.close()

@app.route('/api/revenue', methods=['GET'])
def total_income():
    try:
        connector = get_connection()
        cursor = connector.cursor()

        cursor.execute("SELECT SUM(revenue) FROM sale_record")
        total_revenue = cursor.fetchone()[0] or 0
        
        return jsonify({"total_revenue": round(total_revenue, 2)}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    finally:
        cursor.close()
        connector.close()

@app.route('/api/search', methods=['GET'])
def search_books():
    filter_by = request.args.get('filter_by')
    value = request.args.get('value')
    
    try:
        connector = get_connection()
        cursor = connector.cursor()
        
        if filter_by not in ['title', 'genre', 'author', 'publication']:
            return jsonify({"error": "Invalid filter option."}), 400
        
        query = f"SELECT * FROM available_books WHERE {filter_by} LIKE %s"
        cursor.execute(query, ('%' + value + '%',))
        results = cursor.fetchall()

        book_list = []
        for book in results:
            book_list.append({
                "book_id": book[0],
                "title": book[1],
                "genre": book[2],
                "quantity": book[3],
                "author": book[4],
                "publication": book[5],
                "price": book[6]
            })
        return jsonify(book_list), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    finally:
        cursor.close()
        connector.close()
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    try:
        connector = get_connection()
        cursor = connector.cursor()

        cursor.execute("SELECT * FROM login WHERE username = %s", (username.strip(),))
        user = cursor.fetchone()

        if user is not None and user[1] == password.strip():
            return jsonify({"message": "Login successful."}), 200
        else:
            return jsonify({"error": "Incorrect credentials."}), 401
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    finally:
        cursor.close()
        connector.close()


if __name__ == '__main__':
    app.run(debug=True)