A Django REST Framework API for managing a library system with user authentication, book management, and borrowing functionality.

## Features

- **User Authentication**: JWT-based authentication with registration and login
- **Book Management**: CRUD operations for books (admin-only for create/update/delete)
- **Borrowing System**: Users can borrow and return books
- **Search & Pagination**: Search books by title, author, or ISBN with pagination support
- **Admin Portal**: Django admin interface for managing books and borrows

## Tech Stack

- Django 4.2.7
- Django REST Framework 3.14.0
- SimpleJWT 5.3.0
- SQLite (default database)

## Setup Instructions

### 1. Create and Activate Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin user. This user will be able to create, update, and delete books.

### 5. Run the Development Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## API Endpoints

### Authentication

#### Register User
- **POST** `/register/`
- **Authentication**: Not required
- **Request Body**:
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123",
  "password2": "securepassword123",
  "first_name": "John",
  "last_name": "Doe"
}
```
- **Response**: Returns user data and JWT tokens (access & refresh)

#### Login
- **POST** `/login/`
- **Authentication**: Not required
- **Request Body**:
```json
{
  "username": "john_doe",
  "password": "securepassword123"
}
```
- **Response**: Returns JWT access and refresh tokens

#### Refresh Token
- **POST** `/token/refresh/`
- **Request Body**:
```json
{
  "refresh": "your_refresh_token_here"
}
```

### Books

#### List Books (with pagination and search)
- **GET** `/books/`
- **Authentication**: Required
- **Query Parameters**:
  - `search`: Search by title, author, or ISBN (optional)
  - `page`: Page number for pagination (optional)
- **Example**: `/books/?search=python&page=1`

#### Get Book Details
- **GET** `/books/<id>/`
- **Authentication**: Required

#### Create Book (Admin Only)
- **POST** `/books/`
- **Authentication**: Required (Admin)
- **Request Body**:
```json
{
  "title": "Python Programming",
  "author": "John Smith",
  "isbn": "9780123456789",
  "total_copies": 5,
  "available_copies": 5
}
```

#### Update Book (Admin Only)
- **PUT/PATCH** `/books/<id>/`
- **Authentication**: Required (Admin)

#### Delete Book (Admin Only)
- **DELETE** `/books/<id>/`
- **Authentication**: Required (Admin)

### Borrowing

#### Borrow a Book
- **POST** `/borrow/<book_id>/`
- **Authentication**: Required
- **Response**: Returns borrow details
- **Errors**:
  - 404: Book not found
  - 400: No copies available or already borrowed

#### Return a Book
- **POST** `/return/<book_id>/`
- **Authentication**: Required
- **Response**: Returns updated borrow details
- **Errors**:
  - 404: Book not found
  - 400: No active borrow found

#### View My Borrows
- **GET** `/my-borrows/`
- **Authentication**: Required
- **Response**: List of all borrows (current and past) for the authenticated user

## Usage Examples

### Using cURL

#### 1. Register a new user
```bash
curl -X POST http://127.0.0.1:8000/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password2": "securepassword123"
  }'
```

#### 2. Login
```bash
curl -X POST http://127.0.0.1:8000/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepassword123"
  }'
```

#### 3. List books (with authentication)
```bash
curl -X GET http://127.0.0.1:8000/books/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 4. Search books
```bash
curl -X GET "http://127.0.0.1:8000/books/?search=python" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 5. Borrow a book
```bash
curl -X POST http://127.0.0.1:8000/borrow/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 6. Return a book
```bash
curl -X POST http://127.0.0.1:8000/return/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 7. View my borrows
```bash
curl -X GET http://127.0.0.1:8000/my-borrows/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Using Python requests

```python
import requests

BASE_URL = "http://127.0.0.1:8000"

# Register
response = requests.post(f"{BASE_URL}/register/", json={
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password2": "securepassword123"
})
print(response.json())

# Login
response = requests.post(f"{BASE_URL}/login/", json={
    "username": "john_doe",
    "password": "securepassword123"
})
tokens = response.json()
access_token = tokens['access']

# List books
headers = {"Authorization": f"Bearer {access_token}"}
response = requests.get(f"{BASE_URL}/books/", headers=headers)
print(response.json())

# Borrow a book
response = requests.post(f"{BASE_URL}/borrow/1/", headers=headers)
print(response.json())
```

## Admin Portal

Access the Django admin portal at `http://127.0.0.1:8000/admin/` using your superuser credentials.

The admin portal allows you to:
- Manage books (create, edit, delete)
- View and manage borrows
- Manage users

## Database Models

### Book
- `id`: Primary key
- `title`: Book title
- `author`: Author name
- `isbn`: Unique ISBN (13 characters)
- `total_copies`: Total number of copies
- `available_copies`: Number of available copies
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Borrow
- `id`: Primary key
- `user`: Foreign key to User
- `book`: Foreign key to Book
- `borrowed_date`: When the book was borrowed
- `returned_date`: When the book was returned (null if not returned)
- `is_returned`: Boolean indicating if the book has been returned

## Security Notes

- JWT tokens expire after 1 hour (access) and 1 day (refresh)
- Only authenticated users can access library endpoints
- Only admin users can create, update, or delete books
- Users cannot borrow the same book twice without returning it first

## Testing the API

You can test the API using:
- cURL (command line)
- Postman
- Python requests library
- Django REST Framework's browsable API (visit endpoints in browser when logged in)

