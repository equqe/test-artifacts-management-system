from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from .forms import RegisterForm, ProjectForm
from .models import Projects, TestCases, TestSet, BugReports
from django.urls import reverse_lazy

@login_required
def index_view(request):
    projects = Projects.objects.all()
    return render(request, 'main/index.html', {'projects': projects})

def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'registration/logout.html')

def projects_view(request):
    projects = Projects.objects.all()
    return render(request, 'main/projects.html', {'projects': projects})

def testcase_view(request):
    testcases = TestCases.objects.all()
    return render(request, 'main/testcases.html')

def testset_view(request):
    testsets = TestSet.objects.all()
    return render(request, 'main/testsets.html')

def bugreport_view(request):
    bugreports = BugReports.objects.all()
    return render(request, 'main/bugreports.html')

class ProjectView(FormView):
    form_class = ProjectForm
    template_name = 'main/create_project.html'
    success_url = reverse_lazy('logout')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)