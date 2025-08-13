from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('create/', views.create_event, name='create_event'),
    path('event/<int:pk>/register/', views.register_for_event, name='register_for_event'),
    path('event/<int:pk>/cancel/', views.cancel_event, name='cancel_event'),
    path('statistics/', views.event_statistics, name='event_statistics'),
]
