from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate

# from django.contrib.auth.forms import AuthenticationForm

CustomUser = get_user_model()

class CustomUserRegistrationForm(UserCreationForm):
    agreed_to_terms = forms.BooleanField(
        required=True,
        label="I agree to the Terms and Conditions"
    )
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2','agreed_to_terms']
        widgets = {
            # 'username': forms.TextInput(attrs={'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email'}),
        }
        labels = {
             'username': "Username",
            'email': "Email Address",
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
    

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
class CustomLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Pass the request manually
        super().__init__(*args, **kwargs)

    def clean(self):
        clean_data = super().clean()
        email = clean_data.get('email')
        password = clean_data.get('password')
        if self.request:  # Ensure the request object is available
            user = authenticate(request=self.request, email=email, password=password)
            if user is None:
                raise forms.ValidationError("Invalid email or password.")
        return clean_data
        
