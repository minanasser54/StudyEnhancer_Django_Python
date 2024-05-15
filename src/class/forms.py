from django import forms
from .models import Class,Chapter,Lesson
from ckeditor.widgets import CKEditorWidget

class ClassForm(forms.ModelForm):
    more_info= forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Class
        fields = ['title','more_info','main_subject','tutor','place','day_one','day_two','is_online']

class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['title']
        help_texts = {'title':'chapter name here'}

class LessonForm(forms.ModelForm):
    lessons_text= forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Lesson
        fields = '__all__'
        exclude =['main_class','main_chapter','slug','is_done','notes']

class ChapterGetForm(forms.Form):
    """Django form LessonGet"""
    chapter=forms.CharField(max_length=100)
    help_texts={'chapter':'enter chapter name here'}
