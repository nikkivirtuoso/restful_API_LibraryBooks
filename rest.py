from flask import Flask, request, g
from flask_restful import Resource, Api, reqparse
import sqlite3

app = Flask(__name__)
api = Api(app)


# Database initialization and connection within the Flask context
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('library.db')
    return db

# Create tables and seed database before each request
@app.before_request
def before_request():
    g.db = get_db()
    g.cursor = g.db.cursor()

# Close the database connection after each request
@app.teardown_request
def teardown_request(exception=None):
    if hasattr(g, '_database'):
        g.db.commit()
        g.db.close()

def create_table():
    # Connect to the SQLite database (or create it if it doesn't exist)
    connection = sqlite3.connect('library.db')
    cursor = connection.cursor()

    # Create the 'books' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            publication_year INTEGER
        )
    ''')

    # Commit the changes and close the connection
    connection.commit()
    connection.close()
# Helper function to seed the database with mock data
def seed_database():
    # Connect to the SQLite database
    connection = sqlite3.connect('library.db')
    cursor = connection.cursor()

    # Create the 'books' table if it doesn't exist
    create_table()

    # Insert data into the 'books' table
    cursor.execute("INSERT INTO books (title, author, publication_year) VALUES (?, ?, ?)", ('Book 1', 'Author 1', 2000))

    # Commit the changes and close the connection
    connection.commit()
    connection.close()

# Call the function to create the 'books' table
create_table()

# Call the function to seed the database
seed_database()

# Endpoint 1: Retrieve All Books
class AllBooks(Resource):
    def get(self):
        try:
            g.cursor.execute("SELECT * FROM books")
            books = g.cursor.fetchall()
            return {'books': books}, 200
        except Exception as e:
            return {'error': str(e)}, 500

# Endpoint 2: Add a New Book
class AddBook(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True, help='Title is required')
        parser.add_argument('author', type=str, required=True, help='Author is required')
        parser.add_argument('publication_year', type=int, required=True, help='Publication year is required')

        args = parser.parse_args()

        try:
            g.cursor.execute("INSERT INTO books (title, author, publication_year) VALUES (?, ?, ?)",
                            (args['title'], args['author'], args['publication_year']))
            g.db.commit()
            return {'message': 'Book added successfully'}, 201
        except Exception as e:
            return {'error': str(e)}, 500

# Endpoint 3: Update Book Details
class UpdateBook(Resource):
    def put(self, book_id):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True, help='Title is required')
        parser.add_argument('author', type=str, required=True, help='Author is required')
        parser.add_argument('publication_year', type=int, required=True, help='Publication year is required')

        args = parser.parse_args()

        try:
            g.cursor.execute("UPDATE books SET title=?, author=?, publication_year=? WHERE id=?",
                            (args['title'], args['author'], args['publication_year'], book_id))
            g.db.commit()

            if g.cursor.rowcount == 0:
                return {'error': 'Book not found'}, 404

            return {'message': 'Book updated successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 500

# Add resources to the API
api.add_resource(AllBooks, '/api/books')
api.add_resource(AddBook, '/api/books')
api.add_resource(UpdateBook, '/api/books/<int:book_id>')

# Seed the database with mock data
seed_database()

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
