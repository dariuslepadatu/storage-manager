import psycopg2

# constants for database login
USER='postgres'
PASSWORD='postgres'
HOST='localhost'
PORT='5432'

def databaseAuth(user=USER, password=PASSWORD, host=HOST, port=PORT):
	"""
	Login to the database with specified arguments.
	"""
	# Connect to the database
	conn = psycopg2.connect(user=user,
						password=password, host=host, port=port)

	# create a cursor
	cur = conn.cursor()
	return [conn, cur]


