from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views import *
from .forms import RegisterForm,LogForm
from django.views.generic import CreateView,TemplateView,FormView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.urls import reverse


class LandingView(TemplateView):
   template_name = 'landing.html'

class IndexView(TemplateView):
    template_name="index.html"
    

class LoginView(FormView):
   template_name="log.html"
   form_class=LogForm
   def post(self,request):
      form_data=LogForm(data=request.POST)
      if form_data.is_valid():
         uname=form_data.cleaned_data.get("username")
         pswd=form_data.cleaned_data.get("password")
         user=authenticate(request,username=uname,password=pswd)
         if user:
            print(user)
            login(request,user)
            return redirect("chome")
         else:
            return redirect('log')
      return render(request,'log.html',{"form":form_data})


class RegView(CreateView):
   form_class=RegisterForm
   template_name="reg.html"
   success_url=reverse_lazy("log")
   def form_valid(self, form: BaseModelForm):
      messages.success(self.request,"Registration completed")
      return super().form_valid(form)
   def form_invalid(self, form: BaseModelForm):
      messages.error(self.request,"Registration Failed")
      return super().form_invalid(form)
   

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse("landing"))