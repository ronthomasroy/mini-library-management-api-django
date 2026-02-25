# 📁 Project Structure

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
