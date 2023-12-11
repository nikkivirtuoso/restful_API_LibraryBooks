# Library Management RESTful API

This project implements a simple RESTful API for managing a library system. The API allows users to perform basic CRUD operations on books, interacting with a SQLite database.

## Prerequisites

- Python 3.x
- Flask
- SQLite3 (Included in Python standard library)

## Getting Started

1. Clone the repository:
   git clone https://github.com/nikkivirtuoso/restful_API_LibraryBooks
   cd library-api

Install dependencies:
pip3 install -r requirements.txt

Initialize the database and seed with mock data:
python3 init_db.py

Run the Flask application:
python library_api.py

The API will be accessible at http://127.0.0.1:5000/.

##API Endpoints
1. Retrieve All Books
Endpoint: GET /api/books
Description: Retrieves a list of all books in the library.

3. Add a New Book
Endpoint: POST /api/books
Request Body:
{
  "title": "Book Title",
  "author": "Author Name",
  "publication_year": 2022
}

3. Update Book Details
Endpoint: PUT /api/books/{id}
Request Body:
{
  "title": "Updated Title",
  "author": "Updated Author",
  "publication_year": 2023
}

##Using Postman

Open Postman.
Create a new request.
Set the request type (GET, POST, PUT) and enter the corresponding URL.
Provide the necessary request body (if applicable).
Click "Send" to execute the request.

