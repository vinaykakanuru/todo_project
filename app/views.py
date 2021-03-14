from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.list import ListView
from django.views.generic import View

from app.models import Task
from app.forms import UserForm
from django.contrib.auth import get_user_model
from django.contrib import messages

# Create your views here.

User = get_user_model()


class CustomSignInView(View):
    template_name = "app/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('task-list')
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email_username = request.POST.get('email_username')
        password = request.POST.get('password')

        # trying to login by username or email
        try:
            user_obj = User.objects.get(username=email_username)
            email = user_obj.email
        except Exception:
            email = email_username

        # returns user object from User table if authenticated else None
        user = authenticate(request, email=email, password=password)

        if user is None:
            messages.error(request, 'Invalid Login.')
            return render(request, self.template_name)
        login(request, user)
        return redirect('task-list')


# class CustomLoginView(LoginView):
#     template_name = 'app/login.html'
#     fields = '__all__'
#     redirect_authenticated_user = True

#     def get_success_url(self):
#         return reverse_lazy('task-list')


class RegisterView(FormView):
    template_name = 'app/register.html'
    form_class = UserForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('login')
        return super(RegisterView, self).get(*args, **kwargs)


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    # paginate_by = 2
    # if we don't mention context_object_name then by default it takes "object_list"
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__icontains=search_input)

        context['search_input'] = search_input

        return context


class TaskDetailView(DetailView):
    model = Task
    # if we don't mention context_object_name then by default it takes "object"
    context_object_name = 'task'
    # if we don't mention template_name then by default it takes "appname/modelname_detail.html"
    template_name = 'app/task_detail.html'


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    # default template_name = "appname/modelname_form.html"
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        # Creating task to the logged in user only
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    # default template_name = "appname/modelname_form.html"
    fields = ['title', 'description', 'complete']
    # once task is updated redirecting to task-list page
    success_url = reverse_lazy('task-list')


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    # default template_name = "appname/modelname_complete_delete.html"
    context_object_name = 'task'
    # once task is deleted redirecting to task-list page
    success_url = reverse_lazy('task-list')
