from django.urls import path
from . import views

app_name = 'career'

urlpatterns = [
    path('', views.profession_list, name='profession_list'),
    path('professions/<slug:slug>/', views.profession_detail, name='profession_detail'),
    path('interviews/', views.interview_list, name='interview_list'),
    path('interviews/<slug:slug>/', views.interview_detail, name='interview_detail'),
    path('education/', views.education_path_list, name='education_path_list'),
    path('education/<slug:slug>/', views.education_path_detail, name='education_path_detail'),
    path('vacancies/', views.job_vacancies, name='job_vacancies'),
    path('roadmap/', views.career_roadmap, name='roadmap'),
]
