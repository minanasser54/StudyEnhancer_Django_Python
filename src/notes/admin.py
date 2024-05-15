from django.contrib import admin
from .models import Note
# Register your models here.
class NoteAdmin(admin.ModelAdmin):
    list_filter=["main_lesson",'user','created_at']
    list_display=["main_lesson","user",'created_at']
    search_fields=["note","main_lesson"]
admin.site.register(Note,NoteAdmin)
