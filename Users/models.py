
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager,PermissionsMixin
from django.utils.text import slugify
import uuid
class CustomUserManager(BaseUserManager):
   
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
class CustomUser(AbstractUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # slug = models.SlugField(unique=True, blank=True, null=True)
    
    # Fields specific to job seekers and employers
    is_jobseeker = models.BooleanField(default=False)  
    is_poster = models.BooleanField(default=False)   
    
    # Additional user status fields
    agreed_to_terms = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)   # True if the user's email is verified
    has_company = models.BooleanField(default=False)    # True if the user has a company associated with them
    has_resume = models.BooleanField(default=False)     # True if the job seeker has uploaded a resume
    objects = CustomUserManager()

    # Remove the username requirement by making it optional
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'  # Make email the unique identifier
    REQUIRED_FIELDS = [] 
 
    def __str__(self):
        return self.email or "Unknown Email"
    def save(self, *args, **kwargs):
        print(f"Saving user: {self.email}")
        if not self.email:
            unique_uuid = uuid.uuid4()  
            self.email = f"{unique_uuid}@gmail.com"
        super().save(*args, **kwargs)  

    
    

class JobSeekerProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # slug = models.SlugField(unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    date_of_birth = models.DateField()
    education = models.CharField(max_length=255)
    job = models.CharField(max_length=100)  # Job title
    skills = models.CharField(max_length=100,null=True,blank=True)  # Use a Skill model to store skills
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)  # Job seeker's resume
    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(f"{self.first_name}-{self.last_name}")  # Auto-generate slug
    #     super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.user.username}'s Profile"
    

class EmployerProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # slug = models.SlugField(unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    date_of_birth = models.DateField()
    education = models.CharField(max_length=255)
    job = models.CharField(max_length=100)  # Job title
    company_name = models.CharField(max_length=255)
    company_address = models.CharField(max_length=255)
    company_logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    website = models.URLField(max_length=200)
    industry = models.CharField(max_length=100)
    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(f"{self.first_name}-{self.last_name}")  # Generate slug from job title
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.company_name}'s Profile"

