import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile,Interest


def index(request):
    return render(request, 'social/welcome.html')

def is_strong_password(password):
    """Check if the password is strong."""
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):  # At least one uppercase letter
        return False
    if not re.search(r"[a-z]", password):  # At least one lowercase letter
        return False
    if not re.search(r"[0-9]", password):  # At least one number
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):  # At least one special character
        return False
    return True



@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

def signup(request):
    if request.method == "POST":
        email = request.POST.get('email', '').strip()
        username = request.POST.get('username', '').strip()
        password1 = request.POST.get('password1', '').strip()
        password2 = request.POST.get('password2', '').strip()

        
        if password1 != password2:
            messages.error(request, "Passwords do not match. Please try again.")
            return redirect('signup')  # Redirect back to signup page
        
        if not is_strong_password(password1):
            messages.error(request, "Password must be at least 8 characters long and include an uppercase letter, lowercase letter, number, and special character.")
            return redirect('signup')

        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('signup')

        
        myuser = User.objects.create_user(username=username, password=password1, email=email)
        myuser.save()

        send_mail(
    subject='Welcome to Our TalentHub',
    message='Thank you for signing up. We are glad to have you!',
    from_email=settings.EMAIL_HOST_USER,  
    recipient_list=[email],  
    fail_silently=False,  
)
        messages.success(request, "Your account has been successfully created. A confirmation email has been sent to your email address.")
        return redirect('user_login')

    return render(request, 'social/signup.html', {'messages': messages.get_messages(request)})

def user_login(request):
    if request.method=="POST":
        username=request.POST.get("username","").strip()
        password=request.POST.get("password","").strip()
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
           
            if user.profile.first_time_login:
                
                return redirect('interest')  
            else:
                return redirect('home') 
        else:
            messages.error(request, "Incorrect username or password. Please try again.")
    return render(request, 'social/login.html', {'messages': messages.get_messages(request)})
def interest(request):
    if request.method == "POST":
        selected_interests = request.POST.getlist("interests[]","")

        # Clear previous interests for the user
    

        # Save the selected interests
        for interest_name in selected_interests:
            interest = Interest.objects.create(user=request.user, name=interest_name)
            interest.save()


        # Set the first_time_login flag to False after saving interests
        profile = Profile.objects.get(user=request.user)
        profile.first_time_login = False
        profile.save()

        return redirect('home')  # Redirect to home page after saving interests
    
    return render(request, 'social/interests.html')  # M
       

@login_required
def home(request):
    return render(request,'social/home.html')
@login_required
def logout(request):
    auth_logout(request)  # Logs out the user
    return redirect('user_login')

# def reset(request):
#     return render(request, 'social/reset.html')

# def password_reset_confirm(request):
#     return render(request, 'social/password_reset.html')

