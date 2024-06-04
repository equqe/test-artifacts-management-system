from django.http import Http404, JsonResponse, HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from .forms import RegisterForm, ProjectForm, TestCaseForm, TestsetForm, ReportForm, CaseSetsForm, FilterForm
from .models import Projects, TestCases, TestSet, BugReports, CaseSets
from django.urls import reverse_lazy

pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))

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

from reportlab.pdfgen import canvas

def generate_pdf(data, report_type):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    c = canvas.Canvas(response)

    pdfmetrics.registerFont(TTFont('arial', '/usr/share/fonts/truetype/arial.ttf'))

    if report_type == 'testcases':
        headers = ['ID', 'Название', 'Приоритет', 'Статус', 'Тип кейса', 'Дата создания', 'Автор']
        table_data = [headers] + [[str(item.testcase_id), str(item.name), str(item.priority), str(item.case_status), str(item.case_type), str(item.creation_date.strftime('%d-%m-%Y')), str(item.id)] for item in data]
    else:
        headers = ['ID', 'Приоритет', 'Статус', 'Дата создания', 'Автор', 'Проект', 'ID кейса']
        table_data = [headers] + [[str(item.bug_id), str(item.priority), str(item.status), str(item.creation_date.strftime('%d-%m-%Y')), str(item.id), str(item.project), str(item.testcase_id)] for item in data]

    table = Table(table_data)

    body_style = TableStyle([
        ('FONT', (0, 1), (-1, -1), 'Arial'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
    ])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONT', (0, 0), (-1, 0), 'arial'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    table.setStyle(body_style)

    table_width = table.wrap(0, 0)[0]

    page_width = letter[0]
    x_coord = (page_width - table_width) / 2
    table_height = table.wrap(0, 0)[1]
    page_height = letter[1]
    y_coord = page_height - table_height
    table.drawOn(c, x_coord, y_coord)

    c.save()
    return response



# objects views
def generate_report(request):
    form = FilterForm(request.GET or None)
    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        report_type = form.cleaned_data['report_type']
        search_criteria = form.cleaned_data['search_criteria']

        if report_type == 'testcases':
            data = TestCases.objects.filter(creation_date__range=(start_date, end_date), case_status=search_criteria)
        elif report_type == 'bugreports':
            data = BugReports.objects.filter(creation_date__range=(start_date, end_date))

        if 'download_pdf' in request.GET:
            return generate_pdf(data, report_type)
        else:
            context = {'form': form, 'data': data}
            return render(request, 'main/analytics.html', context)

    return render(request, 'main/analytics.html', {'form': form})

def projects_view(request):
    projects = Projects.objects.all()
    return render(request, 'main/projects.html', {'projects': projects})

def testcase_view(request):
    testcases = TestCases.objects.all()
    return render(request, 'main/testcases.html', {'testcases': testcases})

def testcase_order_view(request, order_by):
    testcases = TestCases.objects.all()
    testcases = testcases.order_by(order_by)
    return render(request, 'main/testcases.html', {'testcases': testcases})

def testset_view(request):
    testsets = TestSet.objects.all()
    return render(request, 'main/testsets.html', {'testsets': testsets})

def testset_order_view(request, order_by, testset_id):
    testset = TestSet.objects.get(pk=testset_id)
    testcases = testset.testcases.order_by(order_by)
    return render(request, 'main/desc_testsets.html', {'testset': testset, 'testcases': testcases})

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
        testset = form.save(commit=False)
        testset.id = self.request.user
        testset.save()
        form.save_m2m()
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
def desc_testset(request, testset_id):
    testset = TestSet.objects.get(pk=testset_id)
    testcases = testset.testcases.all()
    return render(request, 'main/desc_testsets.html', {'testset': testset, 'testcases': testcases})

def add_testcase(request, testset_id):
    testset = TestSet.objects.get(pk=testset_id)
    testcases = TestCases.objects.all()
    
    if request.method == 'POST':
        testcase_ids_str = request.POST.get('testset_testcases')
        testcase_ids = [int(id_str) for id_str in testcase_ids_str.split(',')]
        for testcase_id in testcase_ids:
            testset.testcases.add(TestCases.objects.get(pk=testcase_id))
        testset.save()
    return render(request, 'main/add_testcase.html', {'testset': testset, 'testcases': testcases})




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
        form = form.save(commit=False)
        if self.request.FILES:
            form.testcase_file = self.request.FILES['case_file']
        form.save()
        return super().form_valid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        referer = self.request.META.get('HTTP_REFERER', '/')
        context['referer'] = referer
        return context
    
class edit_testcase_desc(FormView):
    model = TestCases
    form_class = TestCaseForm
    template_name = 'main/desc_edit_testsets.html'
    success_url = reverse_lazy('testsets')

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
        form = form.save(commit=False)
        if self.request.FILES:
            form.testcase_file = self.request.FILES['case_file']
        form.save()
        return super().form_valid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        referer = self.request.META.get('HTTP_REFERER', '/')
        context['referer'] = referer
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
        form = form.save(commit=False)
        form.bug_file = self.request.FILES['bug_file']
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
    form_class = ProjectForm
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