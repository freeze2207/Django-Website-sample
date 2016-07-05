from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^index$', views.index, name='index'),
        url(r'^about', views.about, name='about'),
        url(r'^(?P<item_id>\d+)/$', views.detail, name='detail'),
        url(r'^newitem', views.newitem, name='newitem'),
        url(r'^suggestions', views.suggestions, name='suggestions'),
        url(r'^login', views.user_login, name='login'),
        url(r'^logout', views.user_logout, name='logout'),
        url(r'^myitems', views.myitem, name='myitems'),
        url(r'^register', views.register, name='register'),
        url(r'^info/(?P<suggestion_id>\d+)/$', views.info, name='info'),
        url(r'^searchlib/$', views.searchlib, name='searchlib'),
]
