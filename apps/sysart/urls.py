from django.contrib import admin
from django.urls import path, include
from apps.main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("django.contrib.auth.urls")),
    path('accounts/register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('projects/new/', views.ProjectView.as_view(), name='create_project'),
    path('projects/', views.index_view),
    path('', views.index_view),
]
