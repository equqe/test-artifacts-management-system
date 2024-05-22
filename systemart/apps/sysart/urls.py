from django.contrib import admin
from django.urls import path, include
from apps.main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("django.contrib.auth.urls")),
    path('accounts/register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('projects/', views.projects_view, name='projects'),
    path('projects/new/', views.ProjectView.as_view()),
    path('testcases/', views.testcase_view, name='testcases'),
    path('testcases/new/', views.TestCaseView.as_view()),
    path('testsets/', views.testset_view, name='testsets'),
    path('testsets/new/', views.TestSetView.as_view()),
    path('bugreports/', views.bugreport_view, name='bugreports'),
    path('bugreports/new/', views.BugReportsView.as_view()),
    path('casesets/', views.casesets_view, name='casesets'),
    path('casesets/new/', views.CaseSetsView.as_view()),
    path('', views.index_view),
]
