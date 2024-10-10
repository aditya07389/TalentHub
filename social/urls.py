from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_signup, name='login_signup'),  
    # path('reset/',views.reset,name='reset'),

]
