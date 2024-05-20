import os, io
from flask import Flask, render_template, request, jsonify, send_file, abort
from flask_cors import CORS
from utils import *

app = Flask(__name__)
CORS(app)


@app.route('/products')
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
        return data







if __name__ == '__main__':
	app.run(debug=True)