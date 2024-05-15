from django.shortcuts import render ,get_object_or_404 ,redirect
from .models import Class,MainSubject,Center,Chapter,Lesson
from django.http import FileResponse, Http404,HttpResponse
from django.conf import settings
from django.core.paginator import Paginator
from .filter import ClassFilter
from django.db.models import Q
from .forms import ClassForm,ChapterForm,ChapterGetForm,LessonForm
from accounts.models import Profile
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import datetime
from django.conf import settings
from notes.forms import NoteForm
from notes.models import Note
from django.utils.text import slugify

# Create your views here.
def arabic_slugify(str):
    str = str.replace(" ", "-")
    str = str.replace(",", "-")
    str = str.replace("(", "-")
    str = str.replace(")", "")
    str = str.replace("؟", "")
    str = str.replace("&", "")
    str = str.replace("@", "")
    str = str.replace("#", "")
    str = str.replace("/", "")
    str = str.replace("ء", "")
    str = str.replace("ئ", "")

    return str[1:49]
##viewing data functions
@login_required
def class_list(request):
    class_list=Class.objects.filter(Q(is_active = True)&Q(owner=request.user)).order_by('id')

    filter = ClassFilter(request.GET, queryset=class_list)
    class_list=filter.qs
    paginator = Paginator(class_list, 6) # Show 3 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context={'class_list':page_obj,'filter':filter}
    template="class/class_list.html"
    return render(request,template,context)

@login_required
def class_detail(request,slug):
    class_detail=get_object_or_404(Class,slug=slug)
    chapters=Chapter.objects.filter(main_class=class_detail)
    lessons=Lesson.objects.filter(main_class=class_detail)
    context={'class_detail':class_detail,
             'chapters':chapters,
             'lessons':lessons}
    template="class/class_detail.html"
    return render(request,template,context)

@login_required
def lesson(request,slug):
    lesson=get_object_or_404(Lesson,slug=slug)
    notes=lesson.notes.all().order_by('-created_at')
    context={'lesson':lesson,'notes':notes}
    template="class/lesson.html"
    return render(request,template,context)

@login_required
def pdf(request,slug):
    lesson=get_object_or_404(Lesson,slug=slug)
    path=settings.MEDIA_ROOT[:20]+(lesson.pdf.url.replace('/','\\'))
    print(path)
    try:
        pdf = open(path, "rb").read()
        return HttpResponse(pdf,content_type='application/pdf')
    except:
        raise Http404


@login_required
def mark_done(request,slug):
    lesson=get_object_or_404(Lesson,slug=slug)
    lesson.is_done=True
    lesson.save()
    #lesson=Lesson.objects.filter(slug=slug).update(is_done=True)
    return redirect('/class/l/%s'%slug)

@login_required
def un_done(request,slug):
    lesson=get_object_or_404(Lesson,slug=slug)
    lesson.is_done=False
    lesson.save()
    #lesson=Lesson.objects.filter(slug=slug).update(is_done=False)
    return redirect('/class/l/%s'%slug)


##adding data functions
@login_required
def new_class(request):
    classes=Class.objects.filter(owner=request.user,is_active=True).order_by('-id')
    if request.method=='POST':
        form=ChapterGetForm(request.POST)
        if form.is_valid():
            mydata=request.POST.copy()
            chapter=mydata.get('chapter')
            print(chapter)
            return redirect('/class/new_class/add_lesson/%s'%chapter)

    else:
        form=ChapterGetForm()

    template='add_class/new_class.html'
    context={'classes':classes,'form':form}
    return render(request,template,context)

@login_required
def add_class(request):
    if request.method=='POST':
        form=ClassForm(request.POST)
        if form.is_valid():
            #تخلف سيبك منه
            #sll=form.cleaned_data['slug']
            #myform.slug=arabic_slugify(sll)
            myform=form.save(commit=False)
            myform.owner=request.user
            myform.save()
            clss=Class.objects.filter(owner=request.user).last()
            profile=Profile.objects.get(user=request.user)
            profile.classes.add(clss)
            return redirect('/class/new_class')
    else:
        form=ClassForm()
    context={'form':form}
    template='add_class/add_class_chapter.html'
    return render(request,template,context)

@login_required
def add_chapter(request,slug):
    main_class=Class.objects.get(slug=slug)
    if request.method=='POST':
        form=ChapterForm(request.POST)
        if form.is_valid():
            myform=form.save(commit=False)
            myform.main_class=main_class
            myform.save()
            return redirect('/class/new_class')
    else:
        form=ChapterForm()
    context={'form':form}
    template='add_class/add_class_chapter.html'
    return render(request,template,context)

@login_required
def add_lesson(request,chapter):
    chapter=Chapter.objects.get(title=chapter)
    main_class=Class.objects.get(id=chapter.main_class.id)
    if request.method=='POST':
        form=LessonForm(request.POST,request.FILES)
        if form.is_valid():
            sll=form.cleaned_data['slug']
            myform=form.save(commit=False)
            myform.main_class=main_class
            myform.main_chapter=chapter
            myform.slug=arabic_slugify(sll)
            myform.save()
            return redirect('/class/new_class')
    else:
        form=LessonForm()
    context={'form':form}
    template='add_class/add_class_chapter.html'
    return render(request,template,context)

##editing data functions
@login_required
def edit_class(request,slug):
    main_class=Class.objects.get(slug=slug)
    if request.method=='POST':
        form=ClassForm(request.POST,instance=main_class)
        if form.is_valid():
            tit=slugify(form.cleaned_data['title'])
            ar_slug=arabic_slugify(form.cleaned_data['title'])
            myform=form.save(commit=False)
            myform.owner=request.user
            myform.slug=tit
            if myform.slug:
                myform.save()
                return redirect('/class/inner/%s'%tit)
            else:
                myform.slug=ar_slug
                myform.save()
                return redirect('/class/inner/%s'%ar_slug)
    else:
        form=ClassForm(instance=main_class)
    context={'form':form}
    template='add_class/add_class_chapter.html'
    return render(request,template,context)

@login_required
def edit_chapter(request,slug,id):
    main_class=Class.objects.get(slug=slug)
    chapter=Chapter.objects.get(id=id)
    if request.method=='POST':
        form=ChapterForm(request.POST,instance=chapter)
        if form.is_valid():
            myform=form.save(commit=False)
            myform.main_class=main_class
            myform.save()
            return redirect('/class/inner/%s'%slug)
    else:
        form=ChapterForm(instance=chapter)
    context={'form':form}
    template='add_class/add_class_chapter.html'
    return render(request,template,context)

@login_required
def lesson_edit(request,slug):
    lesson=Lesson.objects.get(slug=slug)
    if request.method=='POST':
        form=LessonForm(request.POST,request.FILES,instance=lesson)
        if form.is_valid():
            tit=slugify(form.cleaned_data['title'])
            ar_slug=arabic_slugify(form.cleaned_data['title'])
            myform=form.save(commit=False)
            myform.slug=tit
            if myform.slug:
                myform.save()
                return redirect('/class/l/%s'%tit)
            else:
                myform.slug=ar_slug
                myform.save()
                return redirect('/class/l/%s'%ar_slug)
    else:
        form=LessonForm(instance=lesson)
    context={'form':form}
    template='add_class/add_class_chapter.html'
    return render(request,template,context)

@login_required
def add_lesson_old_class(request,chapter):
    chapter=Chapter.objects.get(title=chapter)
    main_class=Class.objects.get(id=chapter.main_class.id)
    if request.method=='POST':
        form=LessonForm(request.POST,request.FILES)
        if form.is_valid():
            myform=form.save(commit=False)
            myform.main_class=main_class
            myform.main_chapter=chapter
            myform.save()
            return redirect('/class/inner/%s'%main_class.slug)
    else:
        form=LessonForm()
    context={'form':form}
    template='add_class/add_class_chapter.html'
    return render(request,template,context)

@login_required
def add_chapter_old_class(request,slug):
    main_class=Class.objects.get(slug=slug)
    if request.method=='POST':
        form=ChapterForm(request.POST)
        if form.is_valid():
            myform=form.save(commit=False)
            myform.main_class=main_class
            myform.save()
            return redirect('/class/inner/%s'%slug)
    else:
        form=ChapterForm()
    context={'form':form}
    template='add_class/add_class_chapter.html'
    return render(request,template,context)

@login_required
def del_class(request,slug):
    clas=Class.objects.get(slug=slug)
    clas.delete()
    return redirect('/class')

@login_required
def del_chapter(request,id):
    chapter=Chapter.objects.get(id=id)
    cls=chapter.main_class
    chapter.delete()
    return redirect('/class/inner/%s'%cls.slug)

@login_required
def del_lesson(request,slug):
    lesson=Lesson.objects.get(slug=slug)
    cls=lesson.main_class
    lesson.delete()
    return redirect('/class/inner/%s'%cls.slug)

@login_required
def onlines(request):
    class_list=Class.objects.filter(Q(owner=request.user)&Q(is_online=True)&Q(is_active = True)).order_by('-id')
    filter = ClassFilter(request.GET, queryset=class_list)
    class_list=filter.qs
    paginator = Paginator(class_list, 3) # Show 3 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context={'class_list':page_obj,'filter':filter}
    template="class/class_list.html"
    return render(request,template,context)

@login_required
def add_note(request,slug):
    lesson=Lesson.objects.get(slug=slug)
    if request.method=='POST':
        form=NoteForm(request.POST)
        if form.is_valid():
            ff=form.save(commit=False)
            ff.main_lesson=lesson
            ff.user=lesson.main_class.owner
            ff.save()
            note=Note.objects.filter(main_lesson=lesson).last()
            lesson.notes.add(note)
            return redirect('/class/l/%s'%slug)
    else:
        form=NoteForm()
    return render(request,'add_class/add_class_chapter.html',{'form':form})

@login_required
def undones(request):
    yy=[]
    xx=Lesson.objects.filter(Q(is_done = False)).order_by('-id')
    for lesson in xx:
        if lesson.main_class.owner==request.user:
            yy.append(lesson)
    paginator = Paginator(yy, 3) # Show 3 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,"class/undones.html",{"lessons":page_obj,"yy":yy})
