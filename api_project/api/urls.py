# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, BookList  # Import your ViewSet and previous ListAPIView

# Initialize the router
router = DefaultRouter()

# Register the BookViewSet with the router
router.register(r'books_all', BookViewSet, basename='book_all')

# Define URL patterns
urlpatterns = [
    # Existing route for the BookList view
    path('books/', BookList.as_view(), name='book-list'),

    # Include the router URLs for all CRUD operations
    path('', include(router.urls)),
]
