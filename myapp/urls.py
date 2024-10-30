from django.urls import path

from . import views

urlpatterns = [
    path('updateshorts', views.updateshorts, name='updateshorts'),
    path('', views.updateshorts, name='updateshorts'),
]