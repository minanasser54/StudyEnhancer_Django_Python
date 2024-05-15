from django.urls import path
from . import views
from django.conf.urls import url
app_name='class'
#    path(r'l/^(?P<slug>[-\w]+)$',views.lesson,name='lesson'),

urlpatterns=[
    ##viewing urls
    path('',views.class_list,name='class_list'),
    url(r'^inner/(?P<slug>[-\w]+)/$',views.class_detail,name="class_detail"),
    url(r'^l/(?P<slug>[-\w]+)/$',views.lesson,name="lesson"),

    url(r'^pdf/(?P<slug>[-\w]+)/$',views.pdf,name="pdf"),
    path('onlines/',views.onlines,name='onlines'),
    ##marking lessons
    url(r'^mark_done/(?P<slug>[-\w]+)/$',views.mark_done,name="mark_done"),
    url(r'^un_done/(?P<slug>[-\w]+)/$',views.un_done,name="un_done"),

    ##adding urls
    path('new_class/',views.new_class,name='new_class'),
    path('new_class/add_class/',views.add_class,name='add_class'),
    url(r'^new_class/add_chapter/(?P<slug>[-\w]+)/$',views.add_chapter,name="add_chapter"),
    path('new_class/add_lesson/<str:chapter>/',views.add_lesson,name="add_lesson"),

    ##edit urls
    url(r'^edit_class/(?P<slug>[-\w]+)/(?P<id>\d+)/$',views.edit_chapter,name="edit_chapter"),
    url(r'^edit_class/(?P<slug>[-\w]+)/$',views.edit_class,name="edit_class"),
    url(r'^del_class/(?P<slug>[-\w]+)/$',views.del_class,name="del_class"),
    path('del_chapter/<int:id>',views.del_chapter,name='del_chapter'),

    url(r'^del_lesson/(?P<slug>[-\w]+)/$',views.del_lesson,name="del_lesson"),

    url(r'^edit_class/l/(?P<slug>[-\w]+)/$',views.lesson_edit,name="lesson_edit"),

    path('edit_class/add_lesson_old_class/<str:chapter>',views.add_lesson_old_class,name="add_lesson_old_class"),
    url(r'^edit_class/add_chapter_old_class/(?P<slug>[-\w]+)/$',views.add_chapter_old_class,name="add_chapter_old_class"),

    ##notes
    url(r'^add_note/(?P<slug>[-\w]+)/$',views.add_note,name="add_note"),

    path('undones',views.undones,name='undones'),

]
