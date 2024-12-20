from django.urls import path

from ui import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('blog/', views.blog, name='blog'),
]
