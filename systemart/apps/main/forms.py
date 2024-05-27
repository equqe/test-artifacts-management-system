from django.contrib.auth.forms import UserCreationForm
from django import forms
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
        fields = '__all__' 
        labels = {
            'case_type': 'Тип кейса',
            'priority': 'Приоритет',
            'id': 'Автор',
            'project': 'Проект',
            'name': 'Название',
            'precondition': 'Предусловие',
            'creation_date': 'Дата создания',
        }

        widgets = {
            'creation_date': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
        }


class TestsetForm(forms.ModelForm):
    class Meta:
        model = TestSet
        fields = '__all__' 

        labels = {
            'case_status': 'Статус кейса',
            'set': 'id набора',
            'testcase': 'Кейс',
            'id': 'Автор',
            'runtime': 'Время прохождения',
        }
        
        widgets = {
            'runtime': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
        }


class ReportForm(forms.ModelForm):
    class Meta:
        model = BugReports
        fields = '__all__' 
        labels = {
            'priority': 'Приоритет',
            'status': 'Статус',
            'testcase': 'Кейс',
            'project': 'Проект',
            'name': 'Название',
            'id': 'Автор',
            'description': 'Описание',
            'creationdate': 'Время создания',
        }
        
        widgets = {
            'creationdate': forms.DateInput(attrs={'class':'form-control', 'type':'date', 'placeholder':'YYYY-MM-DD'}),
        }


class CaseSetsForm(forms.ModelForm):
    class Meta:
        model = CaseSets
        fields = '__all__'

        labels = {
            'name': 'Название',
        } 


class FilterForm(forms.Form):
    start_date = forms.DateField(label='Промежуток времени с:')
    end_date = forms.DateField(label='по:')
    report_type = forms.ChoiceField(label='Тип отчета:', choices=[('bugreports', 'Багрепорты'), ('testcases', 'Тесткейсы')])