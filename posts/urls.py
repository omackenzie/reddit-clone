from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_post, name='create_post'),
    path('view/<int:post_id>/', views.view_post, name='view_post'),
    path('create/<int:post_id>/', views.create_comment, name='create_comment'),
    path('vote/<int:post_id>/', views.vote, name='vote'),
]
