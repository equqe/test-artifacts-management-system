from django.http import Http404, HttpResponseNotFound, JsonResponse
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from .forms import RegisterForm, ProjectForm, TestCaseForm, TestsetForm, ReportForm, CaseSetsForm, FilterForm
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
def analytics_view(request):
    testcases = TestCases.objects.all()
    return render(request, 'main/analytics.html', {'testcases': testcases})

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

# desc testset
def desc_testset(request):
    testsets = TestSet.objects.all()
    testcases = TestCases
    return render(request, 'main/testsets.html', {'testsets': testsets})



# delete and edit views

#testcase
def delete_testcase(request, testcase_id):
    password = request.POST.get('password')
    user = authenticate(request, username=request.user.username, password=password)
    print(user, password)
    if user is None:
        return JsonResponse({'success': False, 'error': 'Неверный пароль'})

    testcase = TestCases.objects.get(pk=testcase_id)
    testcase.delete()

    return JsonResponse({'success': True})

class edit_testcase(FormView):
    model = TestCases
    form_class = TestCaseForm
    template_name = 'main/edit_testcase.html'
    success_url = reverse_lazy('testcases')

    def get_object(self):
        obj_id = self.kwargs.get('pk')
        if obj_id:
            try:
                return TestCases.objects.get(pk=obj_id)
            except TestCases.DoesNotExist:
                raise Http404
        else:
            raise Http404

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object()
        return context
    
#testset
def delete_testset(request, testset_id):
    password = request.POST.get('password')
    user = authenticate(request, username=request.user.username, password=password)
    print(user, password)
    if user is None:
        return JsonResponse({'success': False, 'error': 'Неверный пароль'})

    testset = TestSet.objects.get(pk=testset_id)
    testset.delete()

    return JsonResponse({'success': True})

class edit_testset(FormView):
    model = TestSet
    form_class = TestsetForm
    template_name = 'main/edit_testset.html'
    success_url = reverse_lazy('testsets')

    def get_object(self):
        obj_id = self.kwargs.get('pk')
        if obj_id:
            try:
                return TestSet.objects.get(pk=obj_id)
            except TestSet.DoesNotExist:
                raise Http404
        else:
            raise Http404

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object()
        return context
    
#caseset
def delete_caseset(request, set_id):
    password = request.POST.get('password')
    user = authenticate(request, username=request.user.username, password=password)
    print(user, password)
    if user is None:
        return JsonResponse({'success': False, 'error': 'Неверный пароль'})

    testset = CaseSets.objects.get(pk=set_id)
    testset.delete()

    return JsonResponse({'success': True})

class edit_caseset(FormView):
    model = CaseSets
    form_class = CaseSetsForm
    template_name = 'main/edit_caseset.html'
    success_url = reverse_lazy('casesets')

    def get_object(self):
        obj_id = self.kwargs.get('pk')
        if obj_id:
            try:
                return CaseSets.objects.get(pk=obj_id)
            except CaseSets.DoesNotExist:
                raise Http404
        else:
            raise Http404

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object()
        return context
    
#bugreport
def delete_bugreport(request, bug_id):
    password = request.POST.get('password')
    user = authenticate(request, username=request.user.username, password=password)
    print(user, password)
    if user is None:
        return JsonResponse({'success': False, 'error': 'Неверный пароль'})

    testset = BugReports.objects.get(pk=bug_id)
    testset.delete()

    return JsonResponse({'success': True})

class edit_bugreport(FormView):
    model = BugReports
    form_class = ReportForm
    template_name = 'main/edit_bugreport.html'
    success_url = reverse_lazy('bugreports')

    def get_object(self):
        obj_id = self.kwargs.get('pk')
        if obj_id:
            try:
                return BugReports.objects.get(pk=obj_id)
            except BugReports.DoesNotExist:
                raise Http404
        else:
            raise Http404

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object()
        return context
    

#projects
def delete_project(request, project_id):
    password = request.POST.get('password')
    user = authenticate(request, username=request.user.username, password=password)
    print(user, password)
    if user is None:
        return JsonResponse({'success': False, 'error': 'Неверный пароль'})

    testset = Projects.objects.get(pk=project_id)
    testset.delete()

    return JsonResponse({'success': True})

class edit_project(FormView):
    model = Projects
    form_class = ReportForm
    template_name = 'main/edit_project.html'
    success_url = reverse_lazy('projects')

    def get_object(self):
        obj_id = self.kwargs.get('pk')
        if obj_id:
            try:
                return Projects.objects.get(pk=obj_id)
            except Projects.DoesNotExist:
                raise Http404
        else:
            raise Http404

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object()
        return context