from django.urls import path
from app.views import (TaskListView, TaskDetailView, TaskUpdateView, TaskDeleteView, TaskCreateView,
                       CustomSignInView, RegisterView)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomSignInView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    path('', TaskListView.as_view(), name='task-list'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('task-create/', TaskCreateView.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdateView.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', TaskDeleteView.as_view(), name='task-delete'),
]
