from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^index/', views.index),
    url(r'^rewind/', views.rewind),

]