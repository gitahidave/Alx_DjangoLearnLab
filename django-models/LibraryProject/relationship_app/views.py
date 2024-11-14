from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Library  # Importing Library to ensure it's included
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

# Registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log in the user after registration
            login(request, user)
            return redirect('list_books')  # Redirect to a view after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# Function-based view to list all books in the database
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view to display details for a specific library, listing all books available in that library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adding all books related to this library to the context
        context['books'] = self.object.books.all()
        return context

from django.contrib.auth.decorators import permission_required

@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    # add book logic
    pass

@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    # edit book logic
    pass

@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    # delete book logic
    pass