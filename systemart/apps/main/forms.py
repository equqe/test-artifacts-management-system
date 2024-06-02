from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import models
from .models import Tester, Projects, TestCases, TestSet, BugReports, CaseSets
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


class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCases

        step_0 = models.TextField()
        step_1 = models.TextField()
        step_2 = models.TextField()
        step_3 = models.TextField()
        step_4 = models.TextField()
        predictedresult_0 = models.TextField()
        predictedresult_1 = models.TextField()
        predictedresult_2 = models.TextField()
        predictedresult_3 = models.TextField()
        predictedresult_4 = models.TextField()

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
            'predictedresult': 'Ожидаемый результат',
            'step': 'Шаги',
            'case_file': 'Приложение',
        }

        widgets = {
            'creation_date': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'steps': forms.Textarea(attrs={'rows': 10}),  
            'predictedresults': forms.Textarea(attrs={'rows': 10}),  
        }


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
            'runtime': 'Время прохождения',
            'testcase_file': 'Прикрепленный файл',
        }
        
        widgets = {
            'runtime': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'testcases': forms.SelectMultiple(attrs={'class':'form-control', 'label':'Кейсы'}),
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
            'testcase': forms.SelectMultiple(attrs={'class':'form-control', 'label':'Кейсы'}),
        }


class CaseSetsForm(forms.ModelForm):
    class Meta:
        model = CaseSets
        fields = '__all__'

        labels = {
            'name': 'Название',
        } 


class FilterForm(forms.Form):
    start_date = forms.DateField(label='Промежуток времени с:', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='по:', widget=forms.DateInput(attrs={'type': 'date'}))
    report_type = forms.ChoiceField(label='Тип отчета:', choices=[('testcases', 'Тесткейсы'), ('bugreports', 'Багрепорты')])
    search_criteria = forms.ChoiceField(label='Статус:', choices=[('Успешно', 'Успешно'), ('Провален', 'Провален'), ('Пропущен', 'Пропущен'), ('Не пройден', 'Не пройден')])