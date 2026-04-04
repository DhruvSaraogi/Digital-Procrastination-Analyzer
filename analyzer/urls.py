from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Study Sessions
    path('sessions/', views.study_sessions_view, name='study_sessions'),
    path('sessions/delete/<int:pk>/', views.delete_session, name='delete_session'),

    # Distractions
    path('distractions/', views.distractions_view, name='distractions'),

    # Habits
    path('habits/', views.habits_view, name='habits'),
    path('habits/complete/<int:pk>/', views.complete_habit, name='complete_habit'),
    path('habits/delete/<int:pk>/', views.delete_habit, name='delete_habit'),

    # Tasks
    path('tasks/', views.tasks_view, name='tasks'),
    path('tasks/complete/<int:pk>/', views.complete_task, name='complete_task'),
    path('tasks/delete/<int:pk>/', views.delete_task, name='delete_task'),

    # Suggestions
    path('suggestions/', views.suggestions_view, name='suggestions'),
    path('suggestions/rate/<int:pk>/', views.rate_suggestion, name='rate_suggestion'),

    # Alerts
    path('alerts/', views.alerts_view, name='alerts'),
    path('alerts/dismiss/<int:pk>/', views.dismiss_alert, name='dismiss_alert'),

    # Analytics
    path('analytics/', views.analytics_view, name='analytics'),

    # API
    path('api/unread-count/', views.api_unread_count, name='api_unread_count'),
]
