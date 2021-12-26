from django.db import models

from django.contrib.auth.models import AbstractUser  #import Abstract user for create user_type



class User(AbstractUser): #inherite here
    ''' create here user types like teacher , student and admin '''
    is_admin =  models.BooleanField(default=False)
    is_teacher =  models.BooleanField(default=False)
    is_student =  models.BooleanField(default=False)

