from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
choices=(('first prepratory','first prepratory'),
        ('second prepratory','second prepratory'),
        ('third prepratory','third prepratory'),
        ('first secondary','first secondary'),
        ('second secondary','second secondary'),
        ('third secondary','third secondary'))
class Profile(models.Model):
    user  = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile_user')
    slug = models.SlugField(blank=True,null=True,unique=True)
    img = models.ImageField(upload_to="profile_imgs/",blank=True,null=True)
    bio = models.TextField(blank=True,null=True)
    grade= models.PositiveSmallIntegerField(blank=True,null=True)
    education_position = models.CharField(blank=True,null=True,max_length=100,choices=choices)
    classes = models.ManyToManyField('class.Class',blank=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def save(self,*args,**kwargs):
       if not self.slug:
           self.slug=slugify(self.user)
       super(Profile,self).save(*args , **kwargs)

    def __str__(self):
        return str(self.user)

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
