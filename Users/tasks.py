from celery import shared_task
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import generate_token
from .models import CustomUser

@shared_task
def send_welcome_email(email, current_site_domain, user_pk, token):
    # import pdb; pdb.set_trace()
    if not email:
        print("no user")
    subject = 'Welcome to Universal Job Portal!'
    message = (
        f"Hello {email}!\n"
        "Welcome to Universal!\nThank you for visiting our website. "
        "We have sent you a confirmation email; please confirm your email address.\n\n"
        "Thank you,\nUniversal Team"
    )
    from_email = settings.EMAIL_HOST_USER
    
    try:
        # Send the welcome email
        send_mail(subject, message, from_email, [email], fail_silently=True)
        
        user = CustomUser.objects.get(pk=user_pk)  # Fetch the user using user_pk
        print('Send the welcome email--', user.email if user else 'Unknown User')

        # Send the email confirmation link
        email_subject = "Confirm your Email @ Universal - Job Portal Login!"
        message2 = render_to_string('email_confirmation.html', {
            'name': user.email,
            'domain': current_site_domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token,
        })
        send_mail(email_subject, message2, from_email, [email], fail_silently=True)
        
    except CustomUser.DoesNotExist:
        # This exception will be raised if the user does not exist
        raise ValueError(f"User with pk {user_pk} does not exist.")
    except Exception as e:
        print('------------------------exception part--',{email})
        print("Error:", e)
        raise ValueError(f"An error occurred while sending email: {e}")


@shared_task
def send_confirmation_email(user_email, user_pk):
    try:
        user = CustomUser.objects.get(pk=user_pk)  
        token = generate_token.make_token(user)
        print(f"Generated Token for {user_email}: {token}")
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        email_subject = "Confirm your Email @ Universal - Job Portal Login!"
        message2 = render_to_string('email_confirmation.html', {
            'name': user.email,
            'domain': 'http://127.0.0.1:8000/',  
            'uid': uid,
            # 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token,
        })
        
        email = EmailMessage(email_subject,message2,settings.EMAIL_HOST_USER, [user_email],)
        email.send(fail_silently=True)
        
    except CustomUser.DoesNotExist:
        # print(f'User with pk {user_pk} does not exist.')
        raise ValueError(f"User with pk {user_pk} does not exist.")
    except Exception as e:
        # print(f"An error occurred while sending email: {e}")
        raise ValueError(f"An error occurred while sending email: {e}")
