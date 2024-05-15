from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
days_of_week=(('saturday','saturday'),
               ('sunday','sunday'),
               ('monday','monday'),
               ('tuesday','tuesday'),
               ('wednesday','wednesday'),
               ('thursday','thursday'),
               ('friday','friday'))

def arabic_slugify(str):
    str = str.replace(" ", "-")
    str = str.replace(",", "-")
    str = str.replace("(", "-")
    str = str.replace(")", "")
    str = str.replace("؟", "")
    return str

class Center(models.Model):
    name = models.CharField(blank=True, max_length=100)
    phone = models.CharField(blank=True,null=True, max_length=100)
    class Meta:
        verbose_name = 'Center'
        verbose_name_plural = 'Centers'

    def __str__(self):
        return str(self.name)



class Class(models.Model):
     owner = models.ForeignKey(User,on_delete=models.CASCADE,default=1,related_name='class_owner')
     title = models.CharField(max_length=100,unique=True)
     slug = models.SlugField(blank=True,null=True,unique=True)
     more_info = RichTextField(blank=True,null=True)
     main_subject=models.ForeignKey('MainSubject',on_delete=models.CASCADE)
     tutor=models.CharField(blank=True,null=True,max_length=100,default='a teacher')
     place = models.ForeignKey(Center,on_delete=models.DO_NOTHING,blank=True,null=True)
     day_one=models.CharField(max_length=100,choices=days_of_week)
     day_two=models.CharField(max_length=100,choices=days_of_week,blank=True,null=True)
     is_active = models.BooleanField(default=True)
     is_online =  models.BooleanField(default=False)

     class Meta:
         verbose_name='Class'
         verbose_name_plural='Classes'

     def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
            if not self.slug:
                self.slug = arabic_slugify(self.title)
        super(Class,self).save(*args , **kwargs)

     def __str__(self):
         return str(self.title)

class MainSubject(models.Model):
    title = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(blank=True,null=True,unique=True,allow_unicode=True)
    img = models.ImageField(upload_to="sub_imgs/" ,blank=True,null=True)
    book=models.FileField(upload_to="main_sub_books/" ,blank=True,null=True)
    class Meta:
        verbose_name = 'MainSubject'
        verbose_name_plural = 'MainSubjects'

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
        super(MainSubject,self).save(*args , **kwargs)

    def __str__(self):
        return str(self.title)


class Chapter(models.Model):
    title = models.CharField(max_length=100,unique=True)
    main_class= models.ForeignKey(Class,on_delete=models.CASCADE,related_name='chapter_class')
    class Meta:
        verbose_name = 'Chapter'
        verbose_name_plural = 'Chapters'
    def __str__(self):
        return str(self.title)

class Lesson(models.Model):
    main_class= models.ForeignKey(Class,on_delete=models.CASCADE,related_name='lesson_class')
    main_chapter = models.ForeignKey(Chapter,on_delete=models.CASCADE,related_name='lesson_chapter')
    title = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(blank=True,null=True,unique=True,allow_unicode=True)
    sub_subject_name = models.CharField(blank=True,null=True, max_length=100)
    lessons_text = RichTextUploadingField(blank=True,null=True) 
    main_video = models.FileField(blank=True,null=True,upload_to='lesson_videos/')
    second_video = models.FileField(blank=True,null=True,upload_to='lesson_videos/')
    third_video = models.FileField(blank=True,null=True,upload_to='lesson_videos/')
    pdf = models.FileField(blank=True,null=True,upload_to='pdfs/')
    vid1=models.CharField(blank=True,null=True,max_length=200)
    vid2=models.CharField(blank=True,null=True,max_length=200)
    vid3=models.CharField(blank=True,null=True,max_length=200)
    is_done = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    notes = models.ManyToManyField('notes.Note',blank=True)
    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'

    def __str__(self):
        return str(self.title)
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
            if not self.slug:
                self.slug = arabic_slugify(self.title)
        super(Lesson,self).save(*args , **kwargs)
