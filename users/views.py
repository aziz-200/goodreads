from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import View
from .forms import UserCreateForm

app_name = 'users'

class RegisterView(View):

    def get(self,request):
        create_form = UserCreateForm()
        context = {
            "form": create_form
        }
        return render(request, 'users/register.html', context)

    def post(self,request):
        create_form = UserCreateForm(data=request.POST)
        if create_form.is_valid():
            create_form.save()
            return render('users/login.html' )
        else:
            context = {
                "form": create_form
            }
            return render(request, 'users/login.html', context)

class LoginView(View):
    def get(self,request):
        return render(request, 'users/login.html')