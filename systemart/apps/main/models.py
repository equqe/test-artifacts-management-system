from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from datetime import datetime
import uuid

# создание списка уровней приоритета
HIGH = "HI"
MIDDLE = "MD"
LOW = "LW"
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
    LEAD = "LD"  # руководитель тестирования
    SENIOR = "SN" # главный тестировщик
    DEFAULT = "DF"  # обычный тестировщик, стандартная роль
    PROJECT_ROLES_CHOICES = {
        LEAD: "Руководитель тестирования", 
        SENIOR: "Главный тестировщик",
        DEFAULT: "Тестировщик"
    }

    role = models.CharField(
        max_length=2, 
        choices=PROJECT_ROLES_CHOICES, 
        default=DEFAULT
    )
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, null=True, blank=True)


class CaseSets(models.Model):
    """ Модель, описывающая наборы кейсов"""

    set_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)

    def __str__(self):
            return self.name


class TestCases(models.Model):
    """ Модель, описывающая тест-кейсы """

    # создание списка типов кейсов
    FUNCTIONAL = "FU"
    NONFUNCTIONAL = "NF"
    CASE_TYPE_CHOICES = {
        FUNCTIONAL: "Функциональный",
        NONFUNCTIONAL: "Нефункциональный"
    }

    case_type = models.CharField(
        max_length=2,
        choices=CASE_TYPE_CHOICES,
        default=FUNCTIONAL
    )

    priority = models.CharField(
        max_length=2, 
        choices=PRIORITY_CHOICES, 
        default=LOW
    )

    case_id = models.AutoField(primary_key=True)
    id = models.ForeignKey(Tester, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    precondition = models.TextField(max_length=120)
    creation_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
            return self.name


class TestSet(models.Model):
    """ Модель, описывающая тестовые наборы """

    # создание списка статусов кейсов
    SUCCESS = "SC"
    FAIL = "FL"
    SKIP = "SP"
    NPASS = "NP"
    CASE_STATUS_CHOICES = {
        SUCCESS: "Успешно",
        FAIL: "Провален",
        SKIP: "Пропущен",
        NPASS: "Не пройден"
    }

    case_status = models.CharField(
        max_length=2,
        choices=CASE_STATUS_CHOICES,
        default=NPASS
    )

    testset_id = models.AutoField(primary_key=True)
    set = models.ForeignKey(CaseSets, on_delete=models.CASCADE)
    case = models.ForeignKey(TestCases, on_delete=models.CASCADE)
    id = models.ForeignKey(Tester, on_delete=models.CASCADE)
    runtime = models.DateTimeField(default=None, null=True, blank=True)


class CaseSteps(models.Model):
    """ Модель, описывающая шаги кейса """

    step_id = models.AutoField(primary_key=True)
    case = models.ForeignKey(TestCases, on_delete=models.CASCADE)
    step = models.TextField(null=True, blank=True)
    predictedresult = models.TextField(max_length=512)


class BugReports(models.Model):
    """ Модель, описывающая баг репорты """

    # создание списка статусов баг репортов
    OPEN = "OP"
    CLOSED = "CL"
    INPROCESS = "IN"
    BUG_STATUS_CHOICES = {
        OPEN: "Открыт",
        CLOSED: "Закрыт",
        INPROCESS: "В работе"
    }

    status = models.CharField(
        max_length=2,
        choices=BUG_STATUS_CHOICES,
        default=OPEN
    )

    priority = models.CharField(
        max_length=2, 
        choices=PRIORITY_CHOICES, 
        default=LOW
    )

    bug_id = models.AutoField(primary_key=True)
    case = models.ForeignKey(TestCases, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    id = models.ForeignKey(Tester, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=512, null=True, blank=True)
    creationdate = models.DateTimeField(default=datetime.now)

    def __str__(self):
            return self.name