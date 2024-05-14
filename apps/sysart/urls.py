from django.contrib import admin
from django.urls import path, include
from apps.main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("django.contrib.auth.urls")),
    path('accounts/register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.index_view),
]
