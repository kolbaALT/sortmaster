from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('search/', views.search_articles, name='search'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('api/add-comment/', views.add_comment, name='add_comment'),
]
