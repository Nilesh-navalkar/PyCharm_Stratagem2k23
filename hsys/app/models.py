from django.db import models
from django.core.validators import int_list_validator
from django.contrib.auth import get_user_model
user=get_user_model()

# Create your models here.
class profile(models.Model):
    u=models.ForeignKey(user,on_delete=models.CASCADE)
    name=models.TextField()
    email=models.EmailField()
    sap=models.IntegerField()
    pencoding=models.TextField()
    pp=models.ImageField(upload_to="profile",default=None)
    def __str__(self):
        return self.name
    
class attendence(models.Model):
    sap=models.IntegerField()
    date=models.DateField()
    def __str__(self):
        return str(self.date)

