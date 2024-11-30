from django.db import models
from django.utils.text import slugify
from Users.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator
import uuid
class Company(models.Model):
    # Relationship to User model (assuming companies are associated with users)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='company_profile')

    # Company details
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    established_date = models.DateField()
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True, verbose_name="Company Logo")

    # Contact Information
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15, blank=True, null=True)

    # Additional fields
    description = models.TextField(blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)  # e.g., IT, Manufacturing, etc.

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Generate slug from name
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name

class JobType(models.Model):
    JOB_TYPES = [
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('InternShip', 'InternShip')

    ]
    SALARY_RANGE = [
    ('500-1000', '500 - 1,000'),
    ('1000-2000', '1,000 - 2,000'),
    ('2000-3000', '2,000 - 3,000'),
    ('3000-5000', '3,000 - 5,000'),
    ('5000-8000', '5,000 - 8,000'),
    ('8000-10000', '8,000 - 10,000'),
    ('10000-20000', '10,000 - 20,000'),
    ('20000-50000', '20,000 - 50,000'),
    ('50000+', '50,000+'),
  ]

    title = models.CharField(max_length=100,null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Generate slug from job title
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title
    



class Education(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True, null=True)
    institution = models.CharField(max_length=255,null=True,blank=True)
    Highest = models.CharField(max_length=255,null=True,blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.Highest)  # Generate slug from job title
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.user.username} - {self.institution}"
    class Meta:
        verbose_name_plural = "Education"
    
class Skill(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.skill_name)  # Generate slug from job title
        super().save(*args, **kwargs)
    class Meta:
        unique_together = ('user', 'skill_name')
    def __str__(self):
        return f"{self.user.username} - {self.skill_name}"

class Job(models.Model):
    job_title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField()           # Job description
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)  # Optional company
    job_type = models.ForeignKey(JobType,on_delete=models.SET_NULL,null=True, blank=True)  # Job type
    location = models.CharField(max_length=255)  # Job location
    education = models.ForeignKey(Education,on_delete=models.SET_NULL,null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Optional salary
    application_link = models.URLField()  # Link to apply for the job
    rating = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    is_active = models.BooleanField(default=True)  # Flag to indicate if job is active or not
    created_date = models.DateTimeField(auto_now_add=True)  # Date job was created
    last_updated_date = models.DateTimeField(auto_now=True)  # Date job was last updated
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.job_title)  # Generate slug from job title
        super().save(*args, **kwargs)
    def rate_range(self, *args, **kwargs):
        if not (1<=self.rating<=5):
            raise ValueError("Rating should be between 1 and 5")
        super().save(*args, **kwargs)
    def __str__(self):
        return self.job_title
    


    
class Application(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True, null=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add=True)  # Date application was submitted
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.job.job_title}-{self.user.username}-{uuid.uuid4().hex[:8]}")  # Generate slug from job title
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.user.username} applied for {self.job.job_title}"
   
