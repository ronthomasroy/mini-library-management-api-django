from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    BookViewSet,
    register_user,
    borrow_book,
    return_book,
    my_borrows
)

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('borrow/<int:book_id>/', borrow_book, name='borrow'),
    path('return/<int:book_id>/', return_book, name='return'),
    path('my-borrows/', my_borrows, name='my_borrows'),
    path('', include(router.urls)),
]
