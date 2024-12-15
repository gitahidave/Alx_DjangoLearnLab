from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import CustomUser, Post, Comment
from .forms import ProfileForm, CreatePostForm, CommentForm

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = CustomUser
        fields = ['email',]

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})
    
class LoginView(LoginView):
    template_name = 'login.html'

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {'form': form})



@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

class ListView(ListView):
    model = Post
    template_name = 'post_list.html'

class DetailView(DetailView):
    model = Post
    template_name = 'post_view.html'
    context_object_name = 'post'

class CreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_create.html'
    form_class = CreatePostForm
    success_url = '/list/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class UpdateView(UpdateView):
    model = Post
    template_name = 'post_edit.html'

class DeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = 'posts/'
    context_object_name = 'post'

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

class CommentCreateView(CreateView):
    model = Comment
    template_name = 'comment_create.html'
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class CommentUpdateView(UpdateView):
    model = Comment
    template_name = "comment_update.html"

class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'comment_delete.html'


def search(request):
    query = request.GET.get('q') #get the search query from the request
    results = []

    if query:
        #search for posts based on title, content, or tags
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)  # 'tags__name' if using django-taggit
        ).distinct()   # Use distinct to avoid duplicates if a post matches multiple criteria

    return render(request, 'blog/search_results.html', {'query': query, 'results': results})

# view that filters post based on selected tags

class PostByTagListView(ListView):
    model = Post
    template_name = 'blog/posts_by_tag.html'
    context_object_name = 'posts'

    def get_queryset(self):
        tag_name = self.kwargs.get('tag_name')
        return Post.objects.filter(tags__name=tag_name)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_name'] = self.kwargs.get('tag_name')
        return context
