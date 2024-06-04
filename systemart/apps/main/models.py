from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from datetime import datetime
import uuid

# создание списка уровней приоритета
HIGH = "Высокий"
MIDDLE = "Средний"
LOW = "Низкий"
PRIORITY_CHOICES = {
    HIGH: "Высокий", 
    MIDDLE: "Средний",
    LOW: "Низкий",
}

class Projects(models.Model):
    """ Модель, описывающая проекты """
    
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=128)
    description = models.TextField(max_length=120, null=True, blank=True)

    def __str__(self):
        return self.project_name


class Tester(AbstractUser):
    """ Модель, описывающая пользователя """

    # создание списка ролей для проектов
    SENIOR = "Главный тестировщик" # главный тестировщик
    DEFAULT = "Тестировщик"  # обычный тестировщик, стандартная роль
    PROJECT_ROLES_CHOICES = {
        SENIOR: "Главный тестировщик",
        DEFAULT: "Тестировщик"
    }

    role = models.CharField(
        max_length=25, 
        choices=PROJECT_ROLES_CHOICES, 
        default=DEFAULT
    )


class CaseSets(models.Model):
    """ Модель, описывающая наборы кейсов"""

    set_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)

    def __str__(self):
            return self.name


class TestCases(models.Model):
    """ Модель, описывающая тест-кейсы """

    # создание списка типов кейсов
    POSITIVE = "Позитивный"
    NEGATIVE = "Негативный"
    CASE_TYPE_CHOICES = {
        POSITIVE: "Позитивный",
        NEGATIVE: "Негативный"
    }

    # создание списка статусов кейсов
    SUCCESS = "Успешно"
    FAIL = "Провален"
    SKIP = "Пропущен"
    NPASS = "Не пройден"
    CASE_STATUS_CHOICES = {
        SUCCESS: "Успешно",
        FAIL: "Провален",
        SKIP: "Пропущен",
        NPASS: "Не пройден"
    }

    name = models.CharField(max_length=128)

    case_type = models.CharField(
        max_length=10,
        choices=CASE_TYPE_CHOICES,
        default=POSITIVE
    )

    priority = models.CharField(
        max_length=10, 
        choices=PRIORITY_CHOICES, 
        default=LOW
    )

    case_status = models.CharField(
        max_length=10,
        choices=CASE_STATUS_CHOICES,
        default=NPASS,
        null=True, 
        blank=True
    )
    
    testcase_id = models.AutoField(primary_key=True)
    id = models.ForeignKey(Tester, on_delete=models.CASCADE, blank=True, editable=False)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(default=datetime.now, editable=False)
    precondition = models.TextField(max_length=120)
    step_0 = models.TextField(max_length=200, null=True, blank=True)
    step_1 = models.TextField(max_length=200, null=True, blank=True)
    step_2 = models.TextField(max_length=200, null=True, blank=True)
    step_3 = models.TextField(max_length=200, null=True, blank=True)
    step_4 = models.TextField(max_length=200, null=True, blank=True)
    predictedresult_0 = models.TextField(max_length=200, null=True, blank=True)
    predictedresult_1 = models.TextField(max_length=200, null=True, blank=True)
    predictedresult_2 = models.TextField(max_length=200, null=True, blank=True)
    predictedresult_3 = models.TextField(max_length=200, null=True, blank=True)
    predictedresult_4 = models.TextField(max_length=200, null=True, blank=True)
    case_file = models.FileField(upload_to='testcases/', null=True, blank=True)
    runtime = models.DateTimeField(default=datetime.now, editable=False, blank=True)

    def __str__(self):
        return self.name


class TestSet(models.Model):
    """ Модель, описывающая тестовые наборы """
    testset_id = models.AutoField(primary_key=True)
    testset_name = models.CharField(max_length=128)
    testcases = models.ManyToManyField(TestCases, blank=True)
    id = models.ForeignKey(Tester, on_delete=models.CASCADE, blank=True, editable=False)

    def save(self, *args, **kwargs):
        self.runtime = datetime.now()  
        super(TestSet, self).save(*args, **kwargs) 


class BugReports(models.Model):
    """ Модель, описывающая баг репорты """

    # создание списка статусов баг репортов
    OPEN = "Открыт"
    CLOSED = "Закрыт"
    INPROCESS = "В работе"
    BUG_STATUS_CHOICES = {
        OPEN: "Открыт",
        CLOSED: "Закрыт",
        INPROCESS: "В работе"
    }

    name = models.CharField(max_length=128)

    status = models.CharField(
        max_length=10,
        choices=BUG_STATUS_CHOICES,
        default=OPEN
    )

    priority = models.CharField(
        max_length=10, 
        choices=PRIORITY_CHOICES, 
        default=LOW
    )

    bug_id = models.AutoField(primary_key=True)
    testcase = models.ManyToManyField(TestCases)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(default=datetime.now, editable=False)
    id = models.ForeignKey(Tester, on_delete=models.CASCADE, blank=True, editable=False)
    description = models.TextField(max_length=512, null=True, blank=True)
    bug_file = models.FileField(upload_to='bug_reports/', null=True, blank=True)

    def __str__(self):
            return self.name