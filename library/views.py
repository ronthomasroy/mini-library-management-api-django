from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q
from .models import Book, Borrow
from .serializers import BookSerializer, BorrowSerializer, UserRegistrationSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Book.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(author__icontains=search) |
                Q(isbn__icontains=search)
            )
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Set available_copies to total_copies if not provided
        if 'available_copies' not in request.data:
            serializer.validated_data['available_copies'] = serializer.validated_data.get('total_copies', 1)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def borrow_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

    # Check if user already has an active borrow for this book
    active_borrow = Borrow.objects.filter(
        user=request.user,
        book=book,
        is_returned=False
    ).first()

    if active_borrow:
        return Response(
            {'error': 'You already have an active borrow for this book, cannot borrow another of the same'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check if book is available
    if book.available_copies == 0:
        return Response({'error': 'No copies available'}, status=status.HTTP_400_BAD_REQUEST)

    # Create borrow record
    borrow = Borrow.objects.create(user=request.user, book=book)
    book.available_copies -= 1
    book.save()

    serializer = BorrowSerializer(borrow)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def return_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

    # Find active borrow
    borrow = Borrow.objects.filter(
        user=request.user,
        book=book,
        is_returned=False
    ).first()

    if not borrow:
        return Response({'error': 'You do not have an active borrow for this book'}, status=status.HTTP_400_BAD_REQUEST)

    # Return the book
    borrow.is_returned = True
    borrow.returned_date = timezone.now()
    borrow.save()

    book.available_copies += 1
    book.save()

    serializer = BorrowSerializer(borrow)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_borrows(request):
    borrows = Borrow.objects.filter(user=request.user).order_by('-borrowed_date')
    serializer = BorrowSerializer(borrows, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
