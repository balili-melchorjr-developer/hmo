from django.shortcuts import render, redirect

from django.contrib.auth import login, logout, authenticate

from .forms import SignUpForm
from .decorators import unauthenticated_user

from django.contrib import messages
# Create your views here.

@unauthenticated_user
def signup(request):
    form  = SignUpForm()
    if request.POST:
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            context = {'form': form}
  
    template_name = 'register/signup.html'
    context = {'form': form }
    return render(request, template_name, context)

@unauthenticated_user
def signin(request):
    if request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Email or Password is incorrect')

    template_name = 'register/signin.html'
    context = {}
    return render(request, template_name, context)
        

def signout(request):
    logout(request)
    return redirect('signin')


