from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views import View
from config.views import landing
from .forms import UserCreateForm, UserLoginForm

app_name = 'users'

class RegisterView(View):

    def get(self,request):
        create_form = UserCreateForm()
        context = {
            "form": create_form
        }
        return render(request, 'users/register.html', context)

    def post(self, request):
        create_form = UserCreateForm(data=request.POST)
        if create_form.is_valid():
            create_form.save()
            return render(request, 'users/login.html')
        else:
            context = {
                "form": create_form
            }
            return render(request, 'users/register.html', context)

class LoginView(View):
    def get(self,request):
        login_form = AuthenticationForm()
        return render(request, 'users/login.html', {'login_form': login_form})

    def post(self,request):
        print(request.POST['username'], request.POST['password'])
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect(landing)

        return render(request, 'users/login.html', {'login_form': login_form})