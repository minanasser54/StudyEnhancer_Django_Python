from django.contrib import admin
from .models import Class , MainSubject ,Center ,Lesson ,Chapter
# Register your models here.
class ClassAdmin(admin.ModelAdmin):
    list_filter=["owner","is_active",'main_subject']
    list_display=["title","owner","is_online"]
    search_fields=["title","more_info"]

class LessonAdmin(admin.ModelAdmin):
    list_filter=['main_class']
    list_display=["title","main_class","is_online","main_video"]
    search_fields=["title","lessons_text"]

class ChapterAdmin(admin.ModelAdmin):
    list_filter=["main_class"]
    list_display=["title","main_class"]
    search_fields=["title","main_class"]

admin.site.register(Class,ClassAdmin)
admin.site.register(MainSubject)
admin.site.register(Center)
admin.site.register(Lesson,LessonAdmin)
admin.site.register(Chapter,ChapterAdmin)
