from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.weather_dashboard, name='weather_dashboard'),
    path('update/', views.update, name='update'),
    path('update-form/', views.update_weather_data, name='update_weather_data'),
]