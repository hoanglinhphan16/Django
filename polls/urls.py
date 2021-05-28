import django.contrib.auth.urls
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('upload/', views.Upload.as_view(), name='upload'),

]
