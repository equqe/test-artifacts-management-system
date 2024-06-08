from .forms import RegisterForm, ProjectForm, TestCaseForm, TestsetForm, ReportForm, FilterForm, CaseStepForm
from .models import Projects, TestCases, TestSet, BugReports
from django.http import Http404, JsonResponse, HttpResponse
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.defaults import page_not_found, server_error, permission_denied
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from datetime import datetime
from reportlab.lib.units import mm

pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))

def custom_permission_denied(request, exception=None):
    return render(request, 'main/forbidden.html', status=403)

permission_denied = custom_permission_denied

# auth views
@login_required
def index_view(request):
    projects = Projects.objects.all()
    return render(request, 'main/index.html', {'projects': projects})

@login_required
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'registration/logout.html')


from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle

def generate_pdf(data, report_type):
    date = datetime.now().strftime("%B-%Y-%d")
    name = report_type + "-" + date

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{name}.pdf"'

    c = canvas.Canvas(response, pagesize=landscape(letter))

    pdfmetrics.registerFont(TTFont('arial', '/usr/share/fonts/truetype/arial.ttf'))
    body_text_style = getSampleStyleSheet()['BodyText']
    new_body_text_style = ParagraphStyle(name='BodyText', parent=body_text_style, fontName='arial', fontSize=12)

    if report_type == 'testcases':
        headers = ['ID', 'Название', 'Приоритет', 'Статус', 'Тип кейса', 'Дата прохождения', 'Автор']
        table_data = [headers]
        for item in data:
            table_data.append([
                Paragraph(str(item.testcase_id), new_body_text_style),
                Paragraph(str(item.name), new_body_text_style),
                Paragraph(str(item.priority), new_body_text_style),
                Paragraph(str(item.case_status), new_body_text_style),
                Paragraph(str(item.case_type), new_body_text_style),
                Paragraph(str(item.runtime.strftime('%d-%m-%Y')), new_body_text_style),
                Paragraph(str(item.id), new_body_text_style),
            ])
    else:
        headers = ['ID', 'Название', 'Приоритет', 'Статус', 'Дата создания', 'Автор', 'Проект']
        table_data = [headers]
        for item in data:
            table_data.append([
                Paragraph(str(item.bug_id), new_body_text_style),
                Paragraph(str(item.name), new_body_text_style),
                Paragraph(str(item.priority), new_body_text_style),
                Paragraph(str(item.status), new_body_text_style),
                Paragraph(str(item.creation_date.strftime('%d-%m-%Y')), new_body_text_style),
                Paragraph(str(item.id), new_body_text_style),
                Paragraph(str(item.project), new_body_text_style),
            ])
    col_widths = [30, 150, 120, 120, 120, 120, 120]

    table = Table(table_data, colWidths=col_widths)

    body_style = TableStyle([
        ('FONT', (0, 0), (-1, -1), 'arial'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
    ])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONT', (0, 0), (-1, -1), 'arial'), 
        ('FONTSIZE', (0, 0), (-1, -1), 12),  
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    table.setStyle(body_style)

    table_width = table.wrapOn(c, 0, 0)[0]
    page_width = letter[1]  
    x_coord = (page_width - table_width) / 2

    table_height = table.wrapOn(c, 0, 0)[1]
    page_height = letter[0]  
    y_coord = page_height - table_height - 30  
    if y_coord < 30:  
        y_coord = 30

    table.drawOn(c, x_coord, y_coord)

    c.save()
    return response



# objects views
@login_required
def generate_report(request):
    form = FilterForm(request.GET or None)
    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        report_type = form.cleaned_data['report_type']
        search_criteria = form.cleaned_data['search_criteria']
        start_runtime = form.cleaned_data['start_runtime']
        end_runtime = form.cleaned_data['end_runtime']

        if report_type == 'testcases':
            data = TestCases.objects.filter(runtime__range=(start_runtime, end_runtime), case_status=search_criteria)
        elif report_type == 'bugreports':
            data = BugReports.objects.filter(creation_date__range=(start_date, end_date))

        if 'download_pdf' in request.GET:
            return generate_pdf(data, report_type)
        else:
            context = {'form': form, 'data': data}
            return render(request, 'main/analytics.html', context)

    return render(request, 'main/analytics.html', {'form': form})

@login_required
def projects_view(request):
    projects = Projects.objects.all()
    return render(request, 'main/projects.html', {'projects': projects})

@login_required
def testcase_view(request):
    testcases = TestCases.objects.all()
    return render(request, 'main/testcases.html', {'testcases': testcases})

@login_required
def testcase_order_view(request, order_by):
    testcases = TestCases.objects.all()
    testcases = testcases.order_by(order_by)
    return render(request, 'main/testcases.html', {'testcases': testcases})

@login_required
def testset_view(request):
    testsets = TestSet.objects.all()
    return render(request, 'main/testsets.html', {'testsets': testsets})

@login_required
def testset_order_view(request, order_by, testset_id):
    testset = TestSet.objects.get(pk=testset_id)
    testcases = testset.testcases.order_by(order_by)
    return render(request, 'main/desc_testsets.html', {'testset': testset, 'testcases': testcases})

@login_required
def bugreport_view(request):
    bugreports = BugReports.objects.all()
    return render(request, 'main/bugreports.html', {'bugreports': bugreports})

# create views
class ProjectView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    permission_required = 'project.create_project'
    login_url = '/accounts/login/'
    redirect_field_name = 'index'
    form_class = ProjectForm
    template_name = 'main/create_project.html'
    success_url = reverse_lazy('projects')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
 
class TestCaseView(LoginRequiredMixin, FormView):
    form_class = TestCaseForm
    template_name = 'main/create_testcase.html'
    success_url = reverse_lazy('testcases')
    login_url = '/accounts/login/'
    redirect_field_name = 'index'

    def form_valid(self, form):
        test_case = form.save(commit=False)
        if self.request.FILES:
            test_case.testcase_file = self.request.FILES['case_file']
        test_case.id = self.request.user
        test_case.save()
        formset = form.steps_formset(instance=test_case, data=self.request.POST, files=self.request.FILES)

        if formset.is_valid():
            print(self.request.POST)
            formset.save()
            return super().form_valid(form)
        else:
            context = self.get_context_data(form=form, steps_formset=formset)
            context['formset_errors'] = formset.errors

            return self.render_to_response(context)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()
        if self.request.method == 'POST':
            context['steps_formset'] = form.steps_formset(self.request.POST, self.request.FILES)
        else:
            context['steps_formset'] = form.steps_formset()
        return context
    
class TestSetView(LoginRequiredMixin, FormView):
    form_class = TestsetForm
    template_name = 'main/create_testset.html'
    success_url = reverse_lazy('testsets')
    login_url = '/accounts/login/'
    redirect_field_name = 'index'

    testcases = TestCases.objects.all()

    def form_valid(self, form):
        form.instance.id = self.request.user
        testset = form.save(commit=False)
        testset.save()
        form.save_m2m()
        return super().form_valid(form)

class BugReportsView(LoginRequiredMixin, FormView):
    form_class = ReportForm
    template_name = 'main/create_bugreport.html'
    success_url = reverse_lazy('bugreports')
    login_url = '/accounts/login/'
    redirect_field_name = 'index'

    def form_valid(self, form):
        form.instance.id = self.request.user
        form.save()
        return super().form_valid(form)


# reg view
class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save()
        tester_group = Group.objects.get(name='Тестировщик')
        tester_group.user_set.add(user)
        return super().form_valid(form)
    

# desc testset
@login_required
def desc_testset(request, testset_id):
    testset = TestSet.objects.get(pk=testset_id)
    testcases = testset.testcases.all()
    return render(request, 'main/desc_testsets.html', {'testset': testset, 'testcases': testcases})

@login_required
def add_testcase(request, testset_id):
    testset = TestSet.objects.get(pk=testset_id)
    testcases = TestCases.objects.all()
    
    if request.method == 'POST':
        testcase_ids_str = request.POST.get('testset_testcases')
        testcase_ids = [int(id_str) for id_str in testcase_ids_str.split(',')]
        for testcase_id in testcase_ids:
            testset.testcases.add(TestCases.objects.get(pk=testcase_id))
        testset.save()
        return redirect('testsets')
    return render(request, 'main/add_testcase.html', {'testset': testset, 'testcases': testcases})


# delete and edit views

#testcase
@login_required
def delete_testcase(request, testcase_id):
    password = request.POST.get('password')
    user = authenticate(request, username=request.user.username, password=password)
    print(user, password)
    if user is None:
        return JsonResponse({'success': False, 'error': 'Неверный пароль'})

    testcase = TestCases.objects.get(pk=testcase_id)
    testcase.delete()

    return JsonResponse({'success': True})


class edit_testcase(LoginRequiredMixin, UpdateView):
    model = TestCases
    form_class = TestCaseForm
    template_name = 'main/edit_testcase.html'
    success_url = reverse_lazy('testcases')
    login_url = '/accounts/login/'
    redirect_field_name = 'index'

    def get_object(self):
        obj_id = self.kwargs.get('pk')
        if obj_id:
            try:
                return TestCases.objects.get(pk=obj_id)
            except TestCases.DoesNotExist:
                raise Http404
        else:
            raise Http404

    def form_valid(self, form):
        test_case = form.save(commit=False)
        if self.request.FILES:
            test_case.testcase_file = self.request.FILES['case_file']
        test_case.id = self.request.user
        test_case.save()
        formset = form.steps_formset(instance=test_case, data=self.request.POST, files=self.request.FILES)
        if formset.is_valid():
            formset.save()
            return super().form_valid(form)
        else:
            context = self.get_context_data(form=form, steps_formset=formset)
            context['formset_errors'] = formset.errors

            return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()
        test_case = self.get_object()
        if self.request.method == 'POST':
            context['steps_formset'] = form.steps_formset(instance=test_case, data=self.request.POST, files=self.request.FILES)
        else:
            context['steps_formset'] = form.steps_formset(instance=test_case)
        context['test_case'] = test_case
        return context


class edit_testcase_desc(LoginRequiredMixin, FormView):
    model = TestCases
    form_class = TestCaseForm
    template_name = 'main/desc_edit_testsets.html'
    success_url = reverse_lazy('testsets')
    login_url = '/accounts/login/'
    redirect_field_name = 'index'

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
        test_case = self.get_object()
        kwargs['instance'] = test_case
        return kwargs

    def form_valid(self, form):
        test_case = form.save(commit=False)
        if self.request.FILES:
            test_case.testcase_file = self.request.FILES['case_file']
        test_case.id = self.request.user
        test_case.save()
        formset = form.steps_formset(instance=test_case, data=self.request.POST, files=self.request.FILES)
        if formset.is_valid():
            formset.save()
            return super().form_valid(form)
        else:
            context = self.get_context_data(form=form, steps_formset=formset)
            context['formset_errors'] = formset.errors

            return self.render_to_response(context)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()
        test_case = self.get_object()
        if self.request.method == 'POST':
            context['steps_formset'] = form.steps_formset(instance=test_case, data=self.request.POST, files=self.request.FILES)
        else:
            context['steps_formset'] = form.steps_formset(instance=test_case)
        context['test_case'] = test_case
        return context

#testset
@login_required
def delete_testset(request, testset_id):
    password = request.POST.get('password')
    user = authenticate(request, username=request.user.username, password=password)
    print(user, password)
    if user is None:
        return JsonResponse({'success': False, 'error': 'Неверный пароль'})

    testset = TestSet.objects.get(pk=testset_id)
    testset.delete()

    return JsonResponse({'success': True})

def delete_testset_testcase(request, testset_id, testcase_id):
    password = request.POST.get('password')
    user = authenticate(request, username=request.user.username, password=password)
    print(user, password)
    if user is None:
        return JsonResponse({'success': False, 'error': 'Неверный пароль'})

    testset = TestSet.objects.get(pk=testset_id)
    testcase = TestCases.objects.get(pk=testcase_id)
    testset.testcases.remove(testcase)

    return JsonResponse({'success': True})


class edit_testset(LoginRequiredMixin, FormView):
    model = TestSet
    form_class = TestsetForm
    template_name = 'main/edit_testset.html'
    success_url = reverse_lazy('testsets')
    login_url = '/accounts/login/'
    redirect_field_name = 'index'

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
    
#bugreport
@login_required
@permission_required('bugreport.delete_bugreport', raise_exception=True)
def delete_bugreport(request, bug_id):
    password = request.POST.get('password')
    user = authenticate(request, username=request.user.username, password=password)
    print(user, password)
    if user is None:
        return JsonResponse({'success': False, 'error': 'Неверный пароль'})

    testset = BugReports.objects.get(pk=bug_id)
    testset.delete()

    return JsonResponse({'success': True})


class edit_bugreport(LoginRequiredMixin, FormView):
    model = BugReports
    form_class = ReportForm
    template_name = 'main/edit_bugreport.html'
    success_url = reverse_lazy('bugreports')
    login_url = '/accounts/login/'
    redirect_field_name = 'index'

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
        form.bug_file = self.request.FILES.get('bug_file')
        form.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object()
        return context
    

#projects
@login_required
@permission_required('project.delete_project', raise_exception=True)
def delete_project(request, project_id):
    password = request.POST.get('password')
    user = authenticate(request, username=request.user.username, password=password)
    print(user, password)
    if user is None:
        return JsonResponse({'success': False, 'error': 'Неверный пароль'})

    testset = Projects.objects.get(pk=project_id)
    testset.delete()

    return JsonResponse({'success': True})

class edit_project(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    model = Projects
    form_class = ProjectForm
    template_name = 'main/edit_project.html'
    success_url = reverse_lazy('projects')
    login_url = '/accounts/login/'
    redirect_field_name = 'index'
    permission_required = 'project.change_project'

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