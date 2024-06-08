from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import models
from .models import Tester, Projects, TestCases, TestSet, BugReports, CaseSteps
from django.utils import timezone

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta(UserCreationForm.Meta):
        model = Tester
        fields = UserCreationForm.Meta.fields + ("email", )

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Projects
        fields = ['project_name', 'description']
        labels = {
            'project_name': 'Название проекта',
            'description': 'Описание',
        }
        
        widgets = {
            'project_name': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'rows':3}),
        }

class CaseStepForm(forms.ModelForm):
    class Meta:
        model = CaseSteps
        fields = '__all__' 
        labels = {
            'step': 'Шаг',
            'predictedresult': 'Ожидаемый результат',
            'testcase_id' : 'ID тесткейса',
        }


class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCases

        fields = '__all__' 
        labels = {
            'name': 'Название',
            'case_type': 'Тип кейса',
            'priority': 'Приоритет',
            'id': 'Автор',
            'case_status': 'Статус кейса',
            'project': 'Проект',
            'precondition': 'Предусловие',
            'creation_date': 'Дата создания',
            'case_file': 'Приложение',
            'runtime': 'Время прохождения',
        }

        widgets = {
            'creation_date': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'runtime': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(TestCaseForm, self).__init__(*args, **kwargs)
        self.steps_formset = forms.inlineformset_factory(TestCases, CaseSteps, form=CaseStepForm, extra=1)

class TestsetForm(forms.ModelForm):
    class Meta:
        model = TestSet
        fields = '__all__' 

        
        labels = {
            'testset_name':'Название',
            'case_status': 'Статус кейса',
            'set': 'id набора',
            'testcases': 'Кейсы',
            'id': 'Автор',
            'testcase_file': 'Прикрепленный файл',
        }
        
        widgets = {
            'runtime': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'testcases': forms.CheckboxSelectMultiple(),
        }


class ReportForm(forms.ModelForm):
    class Meta:
        model = BugReports
        fields = '__all__' 
        labels = {
            'priority': 'Приоритет',
            'status': 'Статус',
            'testcase': 'Кейсы',
            'project': 'Проект',
            'name': 'Название',
            'id': 'Автор',
            'description': 'Описание',
            'creation_date': 'Время создания',
            'bug_file': 'Прикрепленный файл',
        }
        
        widgets = {
            'creation_date': forms.DateInput(attrs={'class':'form-control', 'type':'date', 'placeholder':'YYYY-MM-DD'}),
            'testcases': forms.CheckboxSelectMultiple(),
        }

class FilterForm(forms.Form):
    start_runtime = forms.DateField(label='Дата прохождения с:', widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    end_runtime = forms.DateField(label='по:', widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    start_date = forms.DateField(label='Дата создания с:', widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    end_date = forms.DateField(label='по:', widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    report_type = forms.ChoiceField(label='Тип отчета:', choices=[('testcases', 'Тест кейсы'), ('bugreports', 'Баг репорты')])
    search_criteria = forms.ChoiceField(label='Статус:', choices=[('Успешно', 'Успешно'), ('Провален', 'Провален'), ('Пропущен', 'Пропущен')])