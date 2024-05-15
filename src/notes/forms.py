from django import forms
from .models import Note
from ckeditor.widgets import CKEditorWidget

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['note']
