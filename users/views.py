from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserCreateForm, UserUpdateForm

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
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, "You have been successfully logged in")
            return redirect("books:list")
        return render(request, 'users/login.html', {'login_form': login_form})

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("users:login")
        return render(request, 'users/profile.html', {'user': request.user})

class LogOutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.info(request, "You have been logged out")
        return redirect('landing')

class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        user_update_form = UserUpdateForm(instance=request.user)
        return render(request, 'users/profile_edit.html', {'form': user_update_form})

    def post(self, request):
        user_update_form = UserUpdateForm(request.POST,
                                          instance=request.user,
                                          files=request.FILES)
        if user_update_form.is_valid():
            user_update_form.save()
            messages.success(request, "You have been successfully updated")
            return redirect('users:profile')
        print(user_update_form.errors)
        return render(request, 'users/profile_edit.html', {'form': user_update_form})