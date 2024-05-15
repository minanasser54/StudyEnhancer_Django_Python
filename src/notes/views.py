from django.shortcuts import render,redirect
from .models import Note
from django.core.paginator import Paginator
from .forms import NoteForm
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify

def arabic_slugify(str):
    str = str.replace(" ", "-")
    str = str.replace(",", "-")
    str = str.replace("(", "-")
    str = str.replace(")", "")
    str = str.replace("؟", "")
    return str
# Create your views here.
@login_required
def notes_page(request):
    notes=Note.objects.filter(user=request.user).order_by('-created_at')
    for note in notes:
        lesson=note.main_lesson
        lesson.notes.add(note)
    paginator = Paginator(notes, 3) # Show 3 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={'notes':page_obj}
    return render(request,'notes_page.html',context)

@login_required
def note_detail(request,slug):
    note=Note.objects.get(slug=slug)
    context={'note':note}
    return render(request,'note_detail.html',context)

@login_required
def delete_note(request,slug):
    note=Note.objects.get(slug=slug)
    note.delete()
    return redirect('/notes')

@login_required
def edit_note(request,slug):
    note=Note.objects.get(slug=slug)
    if request.method=='POST':
        form=NoteForm(request.POST,instance=note)
        if form.is_valid():
            tit=form.cleaned_data['note']
            slug=slugify(tit[:25])
            ar_slug=arabic_slugify(tit[:25])
            myform=form.save(commit=False)
            myform.main_lesson=note.main_lesson
            myform.user=note.user
            myform.slug=slug
            if myform.slug:
                myform.save()
                return redirect('/notes/%s'%slug)
            else:
                myform.slug=ar_slug
                myform.save()
                return redirect('/notes/%s'%ar_slug)
    else:
        form=NoteForm(instance=note)
    context={'form':form}
    return render(request,'edit_note.html',context)
