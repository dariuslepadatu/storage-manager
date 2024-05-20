import os, io
from flask import Flask, render_template, request, jsonify, send_file, abort
from flask_cors import CORS
from utils import *

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    """
    Display data to pyhton server only for debugging.
    """
    [conn, cur] = databaseAuth()
    data = []
    cur.execute('''SELECT * FROM products''')
    conn.commit()
    data.append(cur.fetchall())
    cur.execute('''SELECT * FROM suppliers''')
    conn.commit()
    data.append(cur.fetchall())
    cur.execute('''SELECT * FROM storage''')
    conn.commit()
    data.append(cur.fetchall())
    cur.execute('''SELECT * FROM transactions''')
    conn.commit()
    data.append(cur.fetchall())
    cur.close()
    conn.close()
    return render_template('index.html', data=data)

@app.route('/get_products', methods=['GET'])
def get_products():
    conn, cur = databaseAuth()

    cur.execute('''SELECT * FROM products''')
    conn.commit()
    data = cur.fetchall()
    if not data:
        abort(404, "Error no products")
    else:
        return jsonify(data)

@app.route('/get_products_names', methods=['GET'])
def get_products_names():
    conn, cur = databaseAuth()

    cur.execute('''SELECT id, name FROM products''')
    conn.commit()
    data = cur.fetchall()
    if not data:
        abort(404, "Error no products")
    else:
        return jsonify(data)

@app.route('/get_products_descriptions', methods=['GET'])
def get_products_descriptions():
    conn, cur = databaseAuth()

    cur.execute('''SELECT id, description FROM products''')
    conn.commit()
    data = cur.fetchall()
    if not data:
        abort(404, "Error no products")
    else:
        return jsonify(data)

@app.route('/get_products_suppliers', methods=['GET'])
def get_products_suppliers():
    conn, cur = databaseAuth()

    cur.execute('''SELECT id, supplier_id FROM products''')
    conn.commit()
    data = cur.fetchall()
    if not data:
        abort(404, "Error no products")
    else:
        return jsonify(data)

@app.route('/list_storage', methods=['GET'])
def list_storage():
    conn, cur = databaseAuth()
    name = request.args.get('name')
    supplier = request.args.get('supplier')
    type = request.args.get('type')

    if type:
        cur.execute('''
            SELECT s.row_idx, s.column_idx, p.name AS product_name, p.description AS product_description, 
                   p.supplier_id, sp.name AS supplier_name, sp.description AS supplier_description, t.tr_type, t.tr_date
            FROM storage s
            LEFT JOIN products p ON s.product_id = p.id
            LEFT JOIN suppliers sp ON p.supplier_id = sp.unique_code
            LEFT JOIN transactions t ON t.product_id = p.id
            WHERE t.tr_type = %s
        ''', (type,))
    else:
        query = '''
            SELECT s.row_idx, s.column_idx, p.name AS product_name, p.description AS product_description, 
                   p.supplier_id, sp.name AS supplier_name, sp.description AS supplier_description
            FROM storage s
            LEFT JOIN products p ON s.product_id = p.id
            LEFT JOIN suppliers sp ON p.supplier_id = sp.unique_code
        '''

        if name:
            query += ' WHERE p.name = %s'
            params = (name,)
        elif supplier:
            query += ' WHERE sp.unique_code = %s'
            params = (supplier,)
        else:
            params = None

        cur.execute(query, params)

    conn.commit()
    data = cur.fetchall()

    if not data:
        abort(404, "Error: no products found.")

    else:
        return jsonify(data)

@app.route('/add_to_storage', methods=['POST'])
def add_to_storage():
    conn, cur = databaseAuth()

    row_idx = request.args.get('row_idx')
    column_idx = request.args.get('column_idx')
    product_id = request.args.get('product_id')
    print(row_idx, column_idx, product_id)
    if not row_idx  or not column_idx or not product_id:
        abort(404, "Error arguments are missing")

    else:
        cur.execute('''
            INSERT INTO storage (row_idx, column_idx, product_id) VALUES (%s, %s, %s)
        ''', (row_idx, column_idx, product_id))
        conn.commit()

        cur.close()
        conn.close()
        return jsonify({"message": "Product succesfully added"}), 200



@app.route('/delete_from_storage', methods=['DELETE'])
def delete_from_storage():
    conn, cur = databaseAuth()

    row_idx = request.args.get('row_idx')
    column_idx = request.args.get('column_idx')

    if not row_idx or not column_idx:
        abort(400, "Error arguments are missing")

    else:
        cur.execute('''
            DELETE FROM storage WHERE row_idx = %s AND column_idx = %s
        ''', (row_idx, column_idx))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Product succesfully deleted"}), 200

if __name__ == '__main__':
	app.run(debug=True)