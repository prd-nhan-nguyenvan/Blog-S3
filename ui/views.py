from django.shortcuts import render

from blogapp.models import Blog


# Create your views here.

def home(request):
    return render(request, 'home.html')


def blog(request):
    blogs = Blog.objects.all()
    context = {
        'blogs': blogs
    }
    return render(request, 'blog.html', context)
