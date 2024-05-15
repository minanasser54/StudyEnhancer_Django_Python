from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import mail_admins,send_mail
import datetime
from django.conf import settings
# Create your views here.
@login_required
def contact(request):
    if request.method=='POST':
        subject=request.POST['subject']
        message=request.POST['message']
        email=request.POST['email']
        full='from '+email+' \n '+ message
        mail_admins(
            subject,
            full,
            settings.EMAIL_HOST_USER,
        )
        send_mail(
            'Study Enhancer',
            'We Have Recieved your Mail %s And We will Reply Soon , THanks for your time'%request.user.username,
            settings.EMAIL_HOST_USER,
            [email]
        )
        return redirect('/class')
    return render(request,'contact.html')
