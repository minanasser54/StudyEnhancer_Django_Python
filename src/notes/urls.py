from django.urls import path
from . import views
from django.conf.urls import url

app_name='notes'

urlpatterns=[
    path('',views.notes_page,name='notes_page'),
    url(r'^(?P<slug>[-\w]+)/$',views.note_detail,name="note_detail"),
    url(r'^delete_note/(?P<slug>[-\w]+)/$',views.delete_note,name="delete_note"),
    url(r'^(?P<slug>[-\w]+)/edit$',views.edit_note,name="edit_note"),

]
