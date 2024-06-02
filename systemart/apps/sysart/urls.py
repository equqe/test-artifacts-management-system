from django.contrib import admin
from django.urls import path, include
from apps.main import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("django.contrib.auth.urls")),
    path('accounts/register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.user_logout, name='logout'),

    path('analytics/', views.generate_report, name='analytics'),

    path('projects/', views.projects_view, name='projects'),
    path('projects/new/', views.ProjectView.as_view()),
    path('projects/delete/<int:project_id>/', views.delete_project, name='delete_project'),
    path('projects/<int:pk>/edit/', views.edit_project.as_view(), name='edit_project'),

    path('testcases/', views.testcase_view, name='testcases'),
    path('testcases/new/', views.TestCaseView.as_view()),
    path('testcases/order_by/<str:order_by>/', views.testcase_order_view, name='testcase_order'),
    path('testcases/delete/<int:testcase_id>/', views.delete_testcase, name='delete_testcase'),
    path('testcases/<int:pk>/edit/', views.edit_testcase.as_view(), name='edit_testcase'),

    path('testsets/', views.testset_view, name='testsets'),
    path('testsets/new/', views.TestSetView.as_view()),
    path('testsets/delete/<int:testset_id>/', views.delete_testset, name='delete_testset'),
    path('testsets/<int:pk>/edit/', views.edit_testset.as_view(), name='edit_testset'),
    path('testsets/<int:testset_id>/', views.desc_testset, name='desc_testset'),
    path('testsets/<int:testset_id>/order_by/<str:order_by>/', views.testset_order_view, name='testset_order'),

    path('testsets/testcase/<int:pk>/edit/', views.edit_testcase_desc.as_view(), name='edit_testcase'),

    path('bugreports/', views.bugreport_view, name='bugreports'),
    path('bugreports/new/', views.BugReportsView.as_view()),
    path('bugreports/delete/<int:bug_id>/', views.delete_bugreport, name='delete_bugreport'),
    path('bugreports/<int:pk>/edit/', views.edit_bugreport.as_view(), name='edit_bugreport'),

    path('casesets/', views.casesets_view, name='casesets'),
    path('casesets/new/', views.CaseSetsView.as_view()),
    path('casesets/delete/<int:set_id>/', views.delete_caseset, name='delete_caseset'),
    path('casesets/<int:pk>/edit/', views.edit_caseset.as_view(), name='edit_caseset'),

    path('', views.index_view),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
