from typing import Any
from django import http
from django.shortcuts import render,redirect
from django.views import View
from .forms import UserRegisterForm,UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse

class RegisterView(View):
    form_class=UserRegisterForm
    template_name='accounts/register.html'
    def dispatch(self, request, *args: Any, **kwargs: Any):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form=self.form_class()
        return render(request,self.template_name, context={'form':form})
    
    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            User.objects.create_user(cd['username'],cd['email'],cd['password'])
            messages.success(request,'Registered Successfully','success')
            return redirect('home:home')
        return render(request,self.template_name,context={'form':form})
    

class UserLoginView(View):
    form_class=UserLoginForm
    tempalate_name='accounts/login.html'

    def dispatch(self, request, *args: Any, **kwargs: Any):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self,request):
        form=self.form_class()
        return render(request,self.tempalate_name,context={'form':form})
    
    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user=authenticate(request,username=cd['username'],password=cd['password'])
            if user is not None:
                login(request,user)
                messages.success(request,'logged in successfully', 'success')
                return redirect('home:home')
            messages.error(request, 'password or username is wrong', 'warning')
            return render(request, self.tempalate_name, context={'form':form})

class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request,'Logged out successfully', 'success')
        return redirect('home:home') 
# 
# @login_required(redirect_field_name='home:home', login_url='accounts/login')   ???????????????????????????????
# def user_logout(request):
#     logout(request)
#     return HttpResponse('logged out')


class UserProfileView(LoginRequiredMixin,View):
    def get(self,request,user_id):
        user=User.objects.get(id=user_id)
        posts=Post.objects.filter(user=user)
        return render(request,'accounts/profile.html',{'posts':posts} )
