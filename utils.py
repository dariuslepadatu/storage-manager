import psycopg2

USER = 'postgres'
PASSWORD = 'postgres'
HOST = 'localhost'
PORT = '5432'

def database_auth(user=USER, password=PASSWORD, host=HOST, port=PORT):
    """
    Login to the database with specified arguments.
    """
    try:
        # Connect to the database
        conn = psycopg2.connect(user=user, password=password, host=host, port=port)

        # create a cursor
        cur = conn.cursor()
        print("Connected to the database")

        return [conn, cur]
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return None, None

def create_tables():
    """
    Create tables if they don't exist already.
    """
    [conn, cur] = database_auth()
    try:
        # Execute create table commands
        cur.execute("""
            CREATE TABLE IF NOT EXISTS suppliers (
                unique_code VARCHAR PRIMARY KEY,
                name VARCHAR NOT NULL,
                description VARCHAR
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR NOT NULL,
                supplier_id VARCHAR REFERENCES suppliers(unique_code),
                description VARCHAR
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS storage (
                id SERIAL PRIMARY KEY,
                row_idx INT NOT NULL,
                column_idx INT NOT NULL,
                product_id INT REFERENCES products(id),
                UNIQUE (row_idx, column_idx)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id SERIAL PRIMARY KEY,
                product_id INT REFERENCES products(id),
                tr_type VARCHAR CHECK (tr_type IN ('in', 'out')),
                tr_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

        conn.commit()
        print("Tables created successfully")
    except (Exception, psycopg2.Error) as error:
        print("Error creating tables:", error)

