from django.shortcuts import render,redirect
from .models import Profile
from .forms import SignupForm,UserForm,ProfileForm
from django.contrib.auth import authenticate,login
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import datetime
from django.conf import settings
from django.utils.text import slugify

# Create your views here.



def signup(request):
    if request.method=='POST':
        form=SignupForm(request.POST)
        if form.is_valid():
            form.save()
            usname=form.cleaned_data['username']
            uspass=form.cleaned_data['password1']
            user=authenticate(username=usname,password=uspass)
            login(request,user)
            return redirect('/accounts/profile/edit')
    else:
        form=SignupForm()
    return render(request,'signup.html',{'form':form})

@login_required
def profile(request):
    profile=Profile.objects.get(user=request.user)
    classes=profile.classes.filter(is_active = True)
    sat=[]
    sun=[]
    mon=[]
    tue=[]
    wed=[]
    thu=[]
    fri=[]
    for clss in classes:
        if (str(clss.day_one) =='saturday')| (str(clss.day_two) == 'saturday'):
            sat.append(clss)
        if (str(clss.day_one) =='sunday')| (str(clss.day_two) == 'sunday'):
            sun.append(clss)
        if (str(clss.day_one) =='monday')| (str(clss.day_two) == 'monday'):
            mon.append(clss)
        if (str(clss.day_one) =='tuesday')| (str(clss.day_two) == 'tuesday'):
            tue.append(clss)
        if (str(clss.day_one) =='wednesday')| (str(clss.day_two) == 'wednesday'):
            wed.append(clss)
        if (str(clss.day_one) =='thursday')| (str(clss.day_two) == 'thursday'):
            thu.append(clss)
        if (str(clss.day_one) =='friday')| (str(clss.day_two) == 'friday'):
            fri.append(clss)

    ### auto table mail algorithm
    rhr=datetime.datetime.now()
    today=rhr.strftime("%a")
    full_name_today=rhr.strftime("%A")
    var=today.lower()
    send_mail('Your Table Today',
                'hello {} {} good {} you have {} today'.format(request.user.first_name,request.user.last_name,full_name_today,vars()[var]),
                settings.EMAIL_HOST_USER,
                [request.user.email],fail_silently=False)

    ### auto praying mail algorithm
    hr_in_f=rhr.strftime("%I")
    hr_in_interval=rhr.strftime("%p")
    comhrs=['08','09','10','11','12']
    if hr_in_f in comhrs:
        send_mail('PrayING Time',
                    '{} come on and start praying to god now never forget .\n you late its {} {}'.format(request.user.username,hr_in_f,hr_in_interval),
                    settings.EMAIL_HOST_USER,
                    [request.user.email],fail_silently=False)

    context={'profile':profile,'sat':sat,'sun':sun,'mon':mon,'tue':tue,'wed':wed,'thu':thu,'fri':fri}
    return render(request,'profile.html',context)

@login_required
def profile_edit(request):
    profile=Profile.objects.get(user=request.user)
    if request.method=='POST':
        userform=UserForm(request.POST,instance=profile.user)
        profileform=ProfileForm(request.POST,request.FILES,instance=profile)
        if userform.is_valid() & profileform.is_valid():
            slug=slugify(request.user)
            userform.save()
            myprofileform=profileform.save(commit=False)
            myprofileform.user=request.user
            myprofileform.slug=slug
            myprofileform.save()
            return redirect('/accounts/profile')
    else:
        userform=UserForm(instance=profile.user)
        profileform=ProfileForm(instance=profile)
    return render(request,'profile_edit.html',{'userform':userform,'profileform':profileform})


def del_account(request,slug):
    profile=Profile.objects.get(Q(user=request.user)&Q(user=request.user))
    profile.delete()
    request.user.delete()
    return redirect('/')
