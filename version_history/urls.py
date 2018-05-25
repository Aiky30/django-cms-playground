from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^create_version/', views.create_version),
    url(r'^rewind/', views.rewind),
]