from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages

def login_signup(request):
    signup_form = UserCreationForm()
    login_form = AuthenticationForm()
    
    if request.method == 'POST':
        if 'signup' in request.POST:
            signup_form = UserCreationForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                messages.success(request, 'Account created successfully!')
                login(request, user)
                return redirect('home')  # Redirect to home page or desired page
            else:
                messages.error(request, 'Error in signup form')
        
        elif 'login' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    print("yeah baby")
                    return redirect('home')  # Redirect to home page or desired page
                else:
                    messages.error(request, 'Invalid username or password')
            else:
                messages.error(request, 'Error in login form')

    return render(request, 'social/login.html', {
        'signup_form': signup_form,
        'login_form': login_form
    })