from django.contrib import admin
from .models import Book, Borrow


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'total_copies', 'available_copies']
    list_filter = ['author', 'created_at']
    search_fields = ['title', 'author', 'isbn']


@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'borrowed_date', 'returned_date', 'is_returned']
    list_filter = ['is_returned', 'borrowed_date']
    search_fields = ['user__username', 'book__title']
