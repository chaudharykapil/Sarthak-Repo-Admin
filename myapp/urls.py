from django.urls import path

from . import views

urlpatterns = [
    path('updateshorts', views.updateshorts, name='updateshorts'),
    path('', views.updateshorts, name='updateshorts'),
    path('edit/post', views.ShoweditPost, name='showeditpost'),
    path('edit/_post',view=views.editPost,name="editpost")
]