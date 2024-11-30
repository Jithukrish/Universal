from django.contrib import admin
from django.urls import path,include
from .views import commanPageView,HomePageView,LoginView,JobSeekerRegistrationView,EmployerRegistrationView
from . import views
urlpatterns = [
    path('activate/<uidb64>/<token>/', views.activate, name='activate'), 
    path('', HomePageView.as_view(), name='home-page'), 
    path('Signin/', LoginView.as_view(), name='login'), 
    # path('Signup/', RegistrationView.as_view(), name='registration'),    
    path('Common_reg/', commanPageView.as_view(), name='Common_page'),  
    path('register/jobseeker/', JobSeekerRegistrationView.as_view(), name='jobseeker_register'),
    path('register/employer/', EmployerRegistrationView.as_view(), name='employer_register'),  
]