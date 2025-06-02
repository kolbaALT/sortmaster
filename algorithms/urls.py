from django.urls import path
from . import views

app_name = 'algorithms'

urlpatterns = [
    path('', views.algorithm_list, name='list'),
    path('<int:algorithm_id>/', views.algorithm_detail, name='detail'),
    path('<int:algorithm_id>/simulator/', views.simulator, name='simulator'),
    path('comparison/', views.comparison, name='comparison'),
    path('api/save-simulation/', views.save_simulation, name='save_simulation'),
]
