from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor.fields import RichTextField

def arabic_slugify(str):
    str = str.replace(" ", "-")
    str = str.replace(",", "-")
    str = str.replace("(", "-")
    str = str.replace(")", "")
    str = str.replace("؟", "")
    return str
# Create your models here.
class Note(models.Model):
    main_lesson = models.ForeignKey('class.Lesson',on_delete=models.CASCADE,related_name='note_lesson')
    note = models.TextField(max_length=1000,unique=True)
    user  = models.ForeignKey(User,on_delete=models.CASCADE,related_name='note_user')
    created_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True,null=True,unique=True,allow_unicode=True)

    class Meta:
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.note[:25])
            if not self.slug:
                self.slug = arabic_slugify(self.note[:25])
        super(Note,self).save(*args , **kwargs)

    def __str__(self):
        return str(self.main_lesson)
