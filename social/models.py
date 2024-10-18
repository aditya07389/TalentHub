from django.db import models
from django.contrib.auth.models import User

class Interest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name 
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_time_login = models.BooleanField(default=True)  

    def __str__(self):
        return self.user.username