from django.db import models
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint, Q


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.author}"

    def save(self, *args, **kwargs):
        # Ensure available_copies doesn't exceed total_copies
        if self.available_copies > self.total_copies:
            self.available_copies = self.total_copies
        super().save(*args, **kwargs)


class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrows')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrows')
    borrowed_date = models.DateTimeField(auto_now_add=True)
    returned_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    class Meta:
        ordering = ['-borrowed_date']
        constraints = [
            UniqueConstraint(
                fields=['user', 'book'],
                condition=Q(is_returned=False),
                name='unique_active_borrow'
            )
        ]

    def __str__(self):
        status = "Returned" if self.is_returned else "Borrowed"
        return f"{self.user.username} - {self.book.title} ({status})"
