from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.views.generic import TemplateView

__author__ = 'Administrator'



urlpatterns = [
    #url('^$', TemplateView.as_view(template_name="homepage.html"), name="index"),
    url(r'^homepage/', views.homepage, name='homepage'),
    url(r'^admin_login/', views.admin_login, name='admin_login'),
    url(r'^reader_home/', views.reader_home, name='reader_home'),
    url(r'^reader_search/', views.reader_search, name='reader_search'),
    url(r'^reader_lending/', views.reader_lending, name='reader_lending'),
    #url(r'^reader_recoverpwd/', views.reader_recoverpwd, name='reader_recoverpwd'),
    url(r'^reader_returnhistory/', views.reader_returnhistory, name='reader_returnhistory'),
    url(r'^reader_lookupfine/', views.reader_lookupfine, name='reader_lookupfine'),
    url(r'^reader_reserve/', views.reader_reserve, name='reader_reserve'),
    url(r'^reader_changeinfo/', views.reader_changeinfo, name='reader_changeinfo'),

    url(r'^admin_home/', views.admin_home, name='admin_home'),
    url(r'^admin_addlibrarian/', views.admin_addlibrarian, name='admin_addlibrarian'),
    url(r'^admin_manage/', views.admin_manage, name='admin_manage'),
    url(r'^admin_defaultvalue/', views.admin_defaultvalue, name='admin_defaultvalue'),
    url(r'^admin_request/', views.admin_request, name='admin_request'),
    url(r'^librarian_home', views.librarian_home, name='librarian_home'),
    url(r'^librarian_managebook', views.librarian_managebook, name='librarian_managebook'),
    url(r'^librarian_addcategory', views.librarian_addcategory, name='librarian_addcategory'),
    url(r'^librarian_changepwd', views.librarian_changepwd, name='librarian_changepwd'),
    url(r'^librarian_addreader', views.librarian_addreader, name='librarian_addreader'),
    url(r'^librarian_managereader', views.librarian_managereader, name='librarian_managereader'),
    url(r'^librarian_checkincome', views.librarian_checkincome, name='librarian_checkincome'),
    url(r'^librarian_post', views.librarian_post, name='librarian_post'),
    url(r'^librarian_lend', views.librarian_lend, name='librarian_lend'),
    url(r'^librarian_return', views.librarian_return, name='librarian_return'),
    url(r'^librarian_addbook', views.librarian_addbook, name='librarian_addbook'),
    url(r'^librarian_deletelist', views.librarian_deletelist, name='librarian_deletelist'),
    url(r'^librarian_editbook', views.librarian_editbook, name='librarian_editbook'),
    url(r'^librarian_checkfine', views.librarian_checkfine, name='librarian_checkfine'),
    url(r'^librarian_checklend', views.librarian_checklend, name='librarian_checklend'),
    url(r'^librarian_checkreturn', views.librarian_checkreturn, name='librarian_checkreturn'),

]
