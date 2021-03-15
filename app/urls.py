from django.contrib.auth.views import (LogoutView, PasswordChangeDoneView,
                                       PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path, reverse_lazy

from app.views import (CustomSignInView, RegisterView, TaskCreateView,
                       TaskDeleteView, TaskDetailView, TaskListView,
                       TaskUpdateView)

urlpatterns = [
    # Authentication URLs
    path('login/', CustomSignInView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    # Task App URLs
    path('', TaskListView.as_view(), name='task-list'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('task-create/', TaskCreateView.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdateView.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', TaskDeleteView.as_view(), name='task-delete'),

    # Password Management URLs
    path('password/reset/',
         PasswordResetView.as_view(
             subject_template_name='app/password_management/password_reset_subject.txt',
             email_template_name='app/password_management/password_reset_email.html',
             template_name='app/password_management/password_reset.html',
         ),
         name='password_reset'),

    path('password/reset/done/',
         PasswordResetDoneView.as_view(
             template_name='app/password_management/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('password/reset/confirm/<uidb64>/<token>',
         PasswordResetConfirmView.as_view(
             template_name='app/password_management/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    path('password/reset/complete/',
         PasswordResetCompleteView.as_view(
             template_name='app/password_management/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    # path('password/change/',
    #      PasswordChangeView.as_view(
    #          template_name='app/password_management/password_change.html',
    #          success_url=reverse_lazy('password_change_done_view')
    #      ),
    #      name='password_change_view'),

    # path('password/change/done/',
    #      PasswordChangeDoneView.as_view(
    #          template_name='app/password_management/password_change_done.html'
    #      ),
    #      name='password_change_done_view'),
]
