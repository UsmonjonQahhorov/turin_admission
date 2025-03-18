from datetime import datetime, timedelta
from hashlib import scrypt
import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.db.models import DateTimeField, Model
import jwt

from apps.users.manager import ApplicantManager
from .choices import GenderChoices, Status, DagreeProgram
import os
from django.db import models
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth.models import AbstractUser
from django.core.cache import cache
from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import ValidationError



class BaseModel(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)  

    class Meta:
        abstract = True



# class ClickOrder(models.Model):
#     is_paid = models.BooleanField(default=False)
#     amount = models.DecimalField(decimal_places=2, max_digits=12)




def user_directory_path(instance, filename):
    return f'temp/{filename}'


class Applicant(BaseModel, AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    birthdate = models.DateField(null=True)
    phone_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=255)
    institution = models.CharField(max_length=150)
    language_certificates = models.CharField(max_length=255, null=True)
    score = models.FloatField(null=True)
    gender = models.CharField(choices=GenderChoices.choices, max_length=100)
    program = models.ForeignKey("Program", on_delete=models.CASCADE, null=True)
    exam_date = models.ForeignKey("ExamDate", on_delete=models.CASCADE)

    file = models.FileField(upload_to=user_directory_path, null=True)
    image = models.ImageField(upload_to=user_directory_path, null=True)
    certificates = models.FileField(upload_to=user_directory_path, null=True)

    is_staff = models.BooleanField(default=False)  
    is_superuser = models.BooleanField(default=False)


    def clean(self):
        if self.exam_date and self.program and self.exam_date not in ExamDate.objects.filter(program=self.program):
            raise ValidationError(f"The selected program '{self.program}' does not have an exam on {self.exam_date}. Please choose a valid exam date.")


    def save(self, *args, **kwargs):
        is_new = self.pk is None
        
        self.clean()
        super().save(*args, **kwargs)
        
        # Create ExamRegistration and ExamAttempt for new applicants
        if is_new and self.program and self.exam_date:
            # Create ExamRegistration
            ExamRegistration.objects.create(
                aplicant=self,  
                program=self.program,
                exam_date=self.exam_date,
                status=Status.PENDING_PAYMENT,
                attempt_number=1,
                result=None,
                ball=None 
            )
            
        
        if is_new:
            new_directory = f"{self.first_name}/"
 
            if self.file:
                new_file_path = os.path.join(new_directory, os.path.basename(self.file.name))
                file_content = self.file.read() 
                default_storage.save(new_file_path, ContentFile(file_content)) 
                self.file.name = new_file_path  

            if self.image:
                new_image_path = os.path.join(new_directory, os.path.basename(self.image.name))
                image_content = self.image.read() 
                default_storage.save(new_image_path, ContentFile(image_content))
                self.image.name = new_image_path  

            if self.certificates:
                new_file_path = os.path.join(new_directory, os.path.basename(self.file.name))
                file_content = self.file.read() 
                default_storage.save(new_file_path, ContentFile(file_content)) 
                self.file.name = new_file_path 

            super().save(update_fields=["file", "image", 'certificates'])     

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.program}"
    
    class Meta:
        verbose_name = ("Applicant")
        verbose_name_plural = ("Applicants")


    def has_module_perms(self, app_label):
        return True


    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = ApplicantManager()



"""aplication model"""    



class Program(models.Model):
    name = models.CharField(max_length=255)
    level = models.CharField(max_length=50, choices=DagreeProgram.choices)
    exam_date = models.ForeignKey("ExamDate", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"
    


class ExamRegion(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class ExamDate(models.Model):
    region = models.ForeignKey(ExamRegion, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.region.name} - {self.date}"
    
class ExamRegistration(models.Model):
    aplicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    exam_date = models.ForeignKey(ExamDate, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING_PAYMENT)
    
    result = models.BooleanField(null=True)
    ball = models.FloatField(null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.aplicant} - {self.program} -({self.status})"
        
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)




# class Document(models.Model):
#     user = models.ForeignKey(Aplicant, on_delete=models.CASCADE)
#     file = models.FileField(upload_to=user_directory_path)
#     image = models.ImageField(upload_to=user_directory_path)
#     uploaded_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user}"
    
    





