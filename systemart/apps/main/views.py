from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from .forms import RegisterForm, ProjectForm, TestCaseForm, TestsetForm, ReportForm, CaseSetsForm
from .models import Projects, TestCases, TestSet, BugReports, CaseSets
from django.urls import reverse_lazy


# auth views
@login_required
def index_view(request):
    projects = Projects.objects.all()
    return render(request, 'main/index.html', {'projects': projects})

def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'registration/logout.html')


# objects views
def projects_view(request):
    projects = Projects.objects.all()
    return render(request, 'main/projects.html', {'projects': projects})

def testcase_view(request):
    testcases = TestCases.objects.all()
    return render(request, 'main/testcases.html', {'testcases': testcases})

def testset_view(request):
    testsets = TestSet.objects.all()
    return render(request, 'main/testsets.html', {'testsets': testsets})

def bugreport_view(request):
    bugreports = BugReports.objects.all()
    return render(request, 'main/bugreports.html', {'bugreports': bugreports})

def casesets_view(request):
    casesets = CaseSets.objects.all()
    return render(request, 'main/casesets.html', {'casesets':casesets})

# create views
class ProjectView(FormView):
    form_class = ProjectForm
    template_name = 'main/create_project.html'
    success_url = reverse_lazy('projects')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
class TestCaseView(FormView):
    form_class = TestCaseForm
    template_name = 'main/create_testcase.html'
    success_url = reverse_lazy('testcases')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
class TestSetView(FormView):
    form_class = TestsetForm
    template_name = 'main/create_testset.html'
    success_url = reverse_lazy('testsets')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class BugReportsView(FormView):
    form_class = ReportForm
    template_name = 'main/create_bugreport.html'
    success_url = reverse_lazy('bugreports')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class CaseSetsView(FormView):
    form_class = CaseSetsForm
    template_name = 'main/create_casesets.html'
    success_url = reverse_lazy('casesets')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# reg view
class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# delete and register views

def delete_testcase(request, testcase_id):
    if request.method == 'POST':
        try:
            testcase = TestCases.objects.get(id=testcase_id)
            testcase.delete()
            return redirect('testcases')
        except TestCases.DoesNotExist:
            return HttpResponseNotFound('Тест-кейс не найден')