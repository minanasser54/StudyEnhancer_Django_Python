from django.contrib import admin
from .models import Profile
from django.contrib.admin.sites import AdminSite

AdminSite.site_header='Study Enhancer Admin'

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_filter=["education_position",'user']
    list_display=["user","education_position"]
    search_fields=["user"]
admin.site.register(Profile,ProfileAdmin)
