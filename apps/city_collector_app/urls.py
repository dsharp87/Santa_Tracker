from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^process', views.process),
    url(r'^$', views.index),
    url(r'^clear$',views.clear),
    url(r'^goHome$', views.goHome),
]
