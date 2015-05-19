from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from eatwhat import views

urlpatterns = patterns('',
    url(r'^$',views.index,name='index'),
    url(r'^djlogin$',views.djlogin,name='login'),
    url(r'^djlogout$',views.djlogout,name='logout'),
    url(r'^vote$',views.vote,name='vote'),
)

