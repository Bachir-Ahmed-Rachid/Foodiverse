from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
def get_redirect_url(user):
    if user.role == 1:
        redirect_url='dashboardVendor'
    elif user.role ==2:
        redirect_url='dashboardCustomer'
    elif user.role is None:
        redirect_url='/admin'
    return redirect_url    


def send_verification_email(request,user,mail_subject,template_path):
    current_site=get_current_site(request)
    message=render_to_string(template_path,{
        'user':user,
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':default_token_generator.make_token(user)
    })
    to_mail=user.email
    mail=EmailMessage(mail_subject,message,to=[to_mail])
    mail.send()


def send_approval_notification(mail_subject,mail_template,context):
    message=render_to_string(mail_template,context)
    to_mail=context['user'].email
    mail=EmailMessage(mail_subject,message,to=[to_mail])
    mail.send()
