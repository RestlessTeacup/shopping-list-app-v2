import sqlite3
import os
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

DB_NAME = 'shopping_list.db'
SQL_SCRIPT_FILE = 'shopping_list.db.sql'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DB_NAME):
        print(f"Creating database '{DB_NAME}' from '{SQL_SCRIPT_FILE}'...")
        with open(SQL_SCRIPT_FILE, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        conn = get_db_connection()
        conn.executescript(sql_script)
        conn.commit()
        conn.close()
        print("Database created.")
    else:
        print(f"Database '{DB_NAME}' exists.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/lists', methods=['GET'])
def get_lists():
    conn = get_db_connection()
    lists = conn.execute('SELECT * FROM shopping_lists').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in lists])

@app.route('/api/lists', methods=['POST'])
def create_list():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({"error": "Name is required"}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO shopping_lists (name, created_date) VALUES (?, DATE("now"))', (name,))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return jsonify({"id": new_id, "name": name}), 201

@app.route('/api/lists/<int:list_id>', methods=['PUT'])
def update_list(list_id):
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({"error": "Name is required"}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE shopping_lists SET name = ? WHERE id = ?', (name, list_id))
    conn.commit()
    conn.close()
    return '', 204

@app.route('/api/lists/<int:list_id>', methods=['DELETE'])
def delete_list(list_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM list_items WHERE list_id = ?', (list_id,))
    cursor.execute('DELETE FROM shopping_lists WHERE id = ?', (list_id,))
    conn.commit()
    conn.close()
    return '', 204

@app.route('/api/lists/<int:list_id>', methods=['GET'])
def get_list_detail(list_id):
    conn = get_db_connection()
    list_info = conn.execute('SELECT * FROM shopping_lists WHERE id = ?', (list_id,)).fetchone()
    if list_info is None:
        conn.close()
        return jsonify({"error": "List not found"}), 404
    query = '''
        SELECT 
            li.id, li.quantity, li.is_purchased,
            p.name as product_name, p.unit,
            s.name as store_name
        FROM list_items li
        JOIN products p ON li.product_id = p.id
        LEFT JOIN stores s ON li.store_id = s.id
        WHERE li.list_id = ?
    '''
    items = conn.execute(query, (list_id,)).fetchall()
    conn.close()
    result = {
        "id": list_info['id'],
        "name": list_info['name'],
        "created_date": list_info['created_date'],
        "items": [dict(ix) for ix in items]
    }
    return jsonify(result)

@app.route('/api/lists/<int:list_id>/items', methods=['POST'])
def add_item_to_list(list_id):
    data = request.get_json()
    product_id = data.get('product_id')
    store_id = data.get('store_id')
    quantity = data.get('quantity', 1)
    if not product_id:
        return jsonify({"error": "product_id is required"}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO list_items (list_id, product_id, store_id, quantity, is_purchased)
        VALUES (?, ?, ?, ?, 0)
    ''', (list_id, product_id, store_id, quantity))
    conn.commit()
    conn.close()
    return jsonify({"message": "Item added"}), 201

@app.route('/api/items/<int:item_id>/toggle', methods=['PUT'])
def toggle_item_status(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT is_purchased FROM list_items WHERE id = ?', (item_id,))
    item = cursor.fetchone()
    if item is None:
        conn.close()
        return jsonify({"error": "Item not found"}), 404
    new_status = 0 if item['is_purchased'] == 1 else 1
    cursor.execute('UPDATE list_items SET is_purchased = ? WHERE id = ?', (new_status, item_id))
    conn.commit()
    conn.close()
    return jsonify({"id": item_id, "is_purchased": bool(new_status)})

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    quantity = data.get('quantity')
    if quantity is None:
        return jsonify({"error": "Quantity required"}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE list_items SET quantity = ? WHERE id = ?', (quantity, item_id))
    conn.commit()
    conn.close()
    return '', 204

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM list_items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return '', 204

@app.route('/api/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return jsonify([dict(p) for p in products])

@app.route('/api/stores', methods=['GET'])
def get_stores():
    conn = get_db_connection()
    stores = conn.execute('SELECT * FROM stores').fetchall()
    conn.close()
    return jsonify([dict(s) for s in stores])

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)