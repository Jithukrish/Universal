from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.views import View
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import UserCreationForm, CustomLoginForm
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import generate_token
from django.conf import settings
# from .tasks import send_welcome_email, send_confirmation_email
from Users.tasks import send_welcome_email, send_confirmation_email
User = get_user_model()
class HomePageView(View):
    def get(self,request):
        return render(request, 'index.html')
class EmployerRegistrationView(View):
    form_class = UserCreationForm
    template_name = 'employreg.html'
    success_url = reverse_lazy('login')

    def get(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, self.template_name)
        return render(request, 'employreg.html', {'content': render_to_string(self.template_name, request=request)})

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
       

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, self.template_name)

        if User.objects.filter(email=email).exists():
            messages.error(request, 'This Email already exists.Please choose another one.')
            return render(request, self.template_name)

        user = User.objects.create_user(email=email, password=password)
  
        user.is_poster = True
        user.is_active = False
        user.save()

        messages.success(request, 'Your Account has been created successfully! Please check your email to confirm your email address and activate your account.'
        )

        try:
            token = generate_token.make_token(user)
            current_site = get_current_site(request)
            send_welcome_email.delay(user.email,current_site.domain,user.pk,token)
            send_confirmation_email.delay(user.email, user.pk)
        except Exception as e:
            print("err--------",e)
            messages.error(request, f"Registration successful, but email could not be sent: {e}")
            return redirect('Common_page')

        return redirect('login')





def activate(request, uidb64, token):
    try:
      
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
        is_valid = default_token_generator.check_token(user, token)
        print(f"Received Token: {token}")
        try:
            if default_token_generator.check_token(user, token):
                user.is_verified = True
                user.save()
                messages.success(request, "Your account has been successfully activated.")
                print('Your account has been successfully activated.')
                return redirect('login') 
            else:
                messages.error(request, "The activation link is invalid or has expired.")
                print('The activation link is invalid or has expired.')
                return redirect('home-page')
        except Exception as e:
            messages.error(request, f"An error occurred while activating the account: {e}")
            print("An error occurred while activating the account: ",e)
            return redirect('Common_page') 

    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist) as e:
        messages.error(request, "Invalid activation link.")
        print("Invalid activation link: ",e)
        return redirect('Common_page')

    

class LoginView(View):
    form_class = CustomLoginForm
    template_name='login.html'
    success_url = reverse_lazy('home')
    def get(self,request) :
        # form = self.form_class()
        form = self.form_class(request=request) 
        return render(request,self.template_name, {'form': form})
    def post(self,request):
        form = self.form_class(data=request.POST)
        print(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request,email=email, password=password)
            if user is not None:
                login(request, user)
                if user.is_jobseeker:
                    return redirect('jobseeker_dashboard')  
                elif user.is_poster:
                    return redirect('employer_dashboard')  
                messages.success(request, 'Login successful.')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        return render(request, self.template_name,{'form': form})

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("home")

class commanPageView(View):
    def get(self,request,*args, **kwargs):
        return render(request, 'Common_Reg.html')

class JobSeekerRegistrationView(View):
    form_class = UserCreationForm
    template_name='JobseekerReg.html'
    # success_url = reverse_lazy('home')
    def get(self, request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, self.template_name)
        return render(request, 'JobseekerReg.html', {'content': render_to_string(self.template_name, request=request)})
    def post(self,request,*args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        if password!=  confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, self.template_name)
        if User.objects.filter(email=email):
            messages.error(request, 'Username already exists')
            return render(request, self.template_name)
        user = User.objects.create_user(email=email, password=password,agreed_to_terms=True)
        user.is_jobseeker = True

        user.save()
        messages.success(request, 'Registration successful. You can now login.')

        subject = 'Welcome to Our Site'
        message = f"Hi {email},\n\nThank you for registering on our platform. We're excited to have you on board!"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list)
            messages.success(request, "Registration successful! Please check your email.")

        except Exception as e:
            messages.error(request, f"Registration successful, but email could not be sent: {e}")

        return redirect('login')   

        







