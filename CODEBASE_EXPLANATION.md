# Codebase Explanation & How to Run

## 📁 Project Structure

```
python_task/
├── library_project/          # Main Django project configuration
│   ├── __init__.py
│   ├── settings.py           # Django settings (database, apps, JWT config)
│   ├── urls.py               # Root URL configuration
│   ├── wsgi.py               # WSGI server configuration
│   └── asgi.py               # ASGI server configuration
│
├── library/                  # Main application (library management)
│   ├── __init__.py
│   ├── models.py             # Database models (Book, Borrow)
│   ├── views.py              # API endpoints logic
│   ├── serializers.py        # Data serialization (JSON conversion)
│   ├── urls.py               # App URL routes
│   ├── admin.py              # Django admin configuration
│   └── apps.py               # App configuration
│
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── README.md                 # API documentation
└── db.sqlite3                # SQLite database (created after migrations)
```

---

## 📄 File-by-File Explanation

### **1. `library_project/settings.py`**
**Purpose**: Main Django configuration file

**Key Settings**:
- **INSTALLED_APPS**: Lists all Django apps (including `rest_framework`, `rest_framework_simplejwt`, and our `library` app)
- **DATABASES**: Uses SQLite (`db.sqlite3`) as the database
- **REST_FRAMEWORK**: Configures DRF with:
  - JWT authentication (users must login to access API)
  - Pagination (10 items per page)
- **SIMPLE_JWT**: JWT token settings (1 hour access, 1 day refresh)

### **2. `library_project/urls.py`**
**Purpose**: Root URL router - connects all URL patterns

**Routes**:
- `/admin/` → Django admin portal
- `/` → Includes all library app URLs

### **3. `library/models.py`**
**Purpose**: Defines database structure (tables and fields)

**Models**:
- **Book**: 
  - Fields: `title`, `author`, `isbn`, `total_copies`, `available_copies`
  - Tracks how many books are available vs total
- **Borrow**:
  - Links a `User` to a `Book`
  - Tracks `borrowed_date`, `returned_date`, `is_returned`
  - Constraint: User can't have multiple active borrows of the same book

### **4. `library/serializers.py`**
**Purpose**: Converts Python objects ↔ JSON for API

**Serializers**:
- **UserRegistrationSerializer**: Handles user signup with password validation
- **BookSerializer**: Converts Book model to/from JSON
- **BorrowSerializer**: Converts Borrow model to/from JSON (includes nested book info)

### **5. `library/views.py`**
**Purpose**: Contains all API endpoint logic

**Endpoints**:
- **BookViewSet**: Full CRUD for books (admin-only for create/update/delete)
  - GET `/books/` - List all books (with search & pagination)
  - GET `/books/<id>/` - Get specific book
  - POST `/books/` - Create book (admin only)
  - PUT/PATCH `/books/<id>/` - Update book (admin only)
  - DELETE `/books/<id>/` - Delete book (admin only)

- **register_user()**: POST `/register/` - User registration
- **borrow_book()**: POST `/borrow/<book_id>/` - Borrow a book
- **return_book()**: POST `/return/<book_id>/` - Return a book
- **my_borrows()**: GET `/my-borrows/` - View user's borrow history

### **6. `library/urls.py`**
**Purpose**: Defines all API endpoint URLs

**URL Patterns**:
- `/register/` → User registration
- `/login/` → JWT login (returns access & refresh tokens)
- `/token/refresh/` → Refresh JWT token
- `/books/` → Book CRUD operations
- `/borrow/<book_id>/` → Borrow a book
- `/return/<book_id>/` → Return a book
- `/my-borrows/` → View user's borrows

### **7. `library/admin.py`**
**Purpose**: Configures Django admin interface

**Features**:
- Admin can view/edit books and borrows
- Search and filter functionality
- Accessible at `/admin/` after creating superuser

### **8. `manage.py`**
**Purpose**: Django's command-line utility

**Common Commands**:
- `python manage.py runserver` - Start development server
- `python manage.py makemigrations` - Create database migration files
- `python manage.py migrate` - Apply migrations to database
- `python manage.py createsuperuser` - Create admin user

---

## 🚀 How to Run the Project

### **Step 1: Activate Virtual Environment**
```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows CMD
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

### **Step 2: Install Dependencies** (if not already done)
```bash
pip install -r requirements.txt
```

### **Step 3: Create Database Tables**
```bash
# Create migration files
python manage.py makemigrations

# Apply migrations to create database
python manage.py migrate
```

This creates `db.sqlite3` with tables for `Book` and `Borrow`.

### **Step 4: Create Admin User** (Optional but recommended)
```bash
python manage.py createsuperuser
```
Follow prompts to create username, email, and password. This user will have admin privileges.

### **Step 5: Start the Server**
```bash
python manage.py runserver
```

The API will be available at: **http://127.0.0.1:8000/**

---

## 🔗 API Endpoints Overview

### **Authentication Endpoints** (No auth required)
- `POST /register/` - Register new user
- `POST /login/` - Login and get JWT tokens

### **Book Endpoints** (Requires JWT token)
- `GET /books/` - List books (supports `?search=query` and pagination)
- `GET /books/<id>/` - Get book details
- `POST /books/` - Create book (admin only)
- `PUT /books/<id>/` - Update book (admin only)
- `DELETE /books/<id>/` - Delete book (admin only)

### **Borrowing Endpoints** (Requires JWT token)
- `POST /borrow/<book_id>/` - Borrow a book
- `POST /return/<book_id>/` - Return a book
- `GET /my-borrows/` - View your borrow history

### **Admin Portal**
- `GET /admin/` - Django admin interface (requires superuser login)

---

## 📝 Quick Test Workflow

1. **Start server**: `python manage.py runserver`

2. **Register a user**:
   ```bash
   curl -X POST http://127.0.0.1:8000/register/ \
     -H "Content-Type: application/json" \
     -d '{"username":"testuser","email":"test@example.com","password":"testpass123","password2":"testpass123"}'
   ```
   Save the `access` token from response.

3. **Login** (alternative):
   ```bash
   curl -X POST http://127.0.0.1:8000/login/ \
     -H "Content-Type: application/json" \
     -d '{"username":"testuser","password":"testpass123"}'
   ```

4. **List books** (use your access token):
   ```bash
   curl -X GET http://127.0.0.1:8000/books/ \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
   ```

5. **Create a book** (as admin):
   - First, make your user admin via Django admin or shell
   - Then use the same token to POST to `/books/`

---

## 🔑 Key Concepts

### **JWT Authentication Flow**:
1. User registers/logs in → Gets `access` and `refresh` tokens
2. Include `access` token in header: `Authorization: Bearer <token>`
3. Token expires after 1 hour → Use `refresh` token to get new `access` token

### **Permissions**:
- **IsAuthenticated**: User must be logged in (all library endpoints)
- **IsAdminUser**: User must be admin (create/update/delete books)

### **Database Relationships**:
- `Borrow` has ForeignKey to `User` and `Book`
- One user can have many borrows
- One book can have many borrows
- Constraint: One active borrow per user-book pair

---

## 🛠️ Common Commands

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver

# Access Django shell (for debugging)
python manage.py shell

# Collect static files (for production)
python manage.py collectstatic
```

---

## 🐛 Troubleshooting

**Import errors in IDE**: 
- Make sure IDE is using venv Python interpreter
- Reload window or select interpreter manually

**Database errors**:
- Run `python manage.py migrate` to create tables

**Permission errors**:
- Make sure you're sending JWT token in Authorization header
- Check if user is admin for create/update/delete operations

**Port already in use**:
- Change port: `python manage.py runserver 8001`

---

## 📚 Additional Resources

- See `README.md` for detailed API documentation
- Django Admin: http://127.0.0.1:8000/admin/
- DRF Browsable API: Visit any endpoint in browser (when logged in)
