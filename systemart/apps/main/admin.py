from django.contrib import admin
from .models import Tester, TestCases, CaseSteps

admin.site.register(Tester)
admin.site.register(TestCases)
admin.site.register(CaseSteps)
