from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    url(r'^view_versions/', views.view_versions),
    url(r'^rewind/', views.rewind),
]