# Imports
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.decorators import user_passes_test, permission_required

# Models
from .models import Library, Book  # Importing Library and Book models

# Utilities for Access Control
def is_admin(user):
    """Check if user has an Admin role."""
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

# Views

# Admin View
# @user_passes_test(is_admin)
# def admin_view(request):
#     """View restricted to Admin users."""
#     return render(request, 'admin_view.html')

# #Librarian View
# def is_librarian(user):
#     return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

# @user_passes_test(is_librarian)
# def librarian_view(request):
#     return render(request, 'librarian_view.html')




# Registration View
def register(request):
    """User registration view with automatic login on success."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')  # Redirect after registration
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# Book Listing View
def list_books(request):
    """List all books available in the library."""
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Library Detail View
class LibraryDetailView(DetailView):
    """Class-based view to display details for a specific library, including all books available in that library."""
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        """Add related books to the context."""
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all()  # Access books related to this library
        return context

# Book Management Views with Permissions

@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    """View to add a new book, restricted by 'can_add_book' permission."""
    # Add book logic here
    pass

@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    """View to edit an existing book, restricted by 'can_change_book' permission."""
    # Edit book logic here
    pass

@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    """View to delete a book, restricted by 'can_delete_book' permission."""
    # Delete book logic here
    pass