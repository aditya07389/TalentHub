"""
URL configuration for talent project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from social import views
from django.contrib.auth import views as auth_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name="index"),
    path('signup/',views.signup,name="signup"),
    path('user_login/',views.user_login,name="user_login"),
    path('logout/', views.logout, name='logout'),
    path('home/',views.home,name="home"),
    # Resetting the password urls
    path('reset/',auth_view.PasswordResetView.as_view(template_name="social/reset.html"),name="reset_password"),
    path('reset_done/',auth_view.PasswordResetDoneView.as_view(template_name="social/reset_done.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>',auth_view.PasswordResetConfirmView.as_view(template_name="social/reset_confirm.html"),name="password_reset_confirm"),
    path('reset_complete/',auth_view.PasswordResetCompleteView.as_view(template_name="social/reset_completed.html"),name="password_reset_complete"),

    path('interest/',views.interest,name="interest")
]
