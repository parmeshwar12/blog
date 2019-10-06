from django.urls import path
from . import views 

app_name = 'post'
urlpatterns = [
    path('',views.home, name='home'),
    path('post/<id>/', views.post, name='post'),
    path('post/<id>/update/', views.post_update, name='post-update'),
    path('post/<id>/delete/', views.post_delete, name='post-delete'),
    path('create/', views.post_create, name='post-create'),
    path('blog/', views.blog, name='blog'),
    path('search/', views.search, name='search'),
    path('contact/', views.contact, name='contact'),
]