from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

# Role-checking function for Librarian
def is_librarian(user):
    """Check if the user has the Librarian role."""
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

@user_passes_test(is_librarian)
def librarian_view(request):
    """View accessible only to users with the Librarian role."""
    return render(request, 'librarian_view.html')