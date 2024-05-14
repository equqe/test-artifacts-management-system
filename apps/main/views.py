from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from .forms import RegisterForm
from django.urls import reverse_lazy

@login_required
def index_view(request):
    return render(request, "main/index.html")

def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'registration/logout.html')

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)