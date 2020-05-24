"""navigus_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import  url
from website import views
from api_views import views as api_views
urlpatterns = [
    path('admin/', admin.site.urls),
    url('loginuser/', api_views.loginuser, name='loginuser'),
    url('signup/', api_views.signup, name='signup'),
    url('signupteacher/', api_views.signupteacher, name='signupteacher'),
    url('getstudentslisting/', api_views.getstudentslisting, name='getstudentslisting'),
    url('getteacherslisting/', api_views.getteacherslisting, name='getteacherslisting'),
    url('gettimeslotslisting/', api_views.gettimeslotslisting, name='gettimeslotslisting'),
   url(r'^makeslots/', api_views.makeslots, name='makeslots'),
   url(r'^getteachertimeslotsbystudent/', api_views.getteachertimeslotsbystudent, name='getteachertimeslotsbystudent'),
   url(r'^bookslot/', api_views.bookslot, name='bookslot'),
    
    
    
    
    
    
    url(r'^$', views.index, name='index'),
    url(r'^dashboard/', views.dashboard, name='dashboard'),
    url(r'^signuptemplate/', views.signuptemplate, name='signuptemplate'),
    url(r'^teachers/', views.teachers, name='teachers'),
    url(r'^students/', views.students, name='students'),
    url(r'^addteacher/', views.addteacher, name='addteacher'),
    
    url(r'^teachertimeslots/', views.teachertimeslots, name='teachertimeslots'),
    
    
    url(r'^logout/', views.logout, name='logout'),
    
    #url('signup/', views.signup, name='signup'),
    #url('dashboard', views.dashboard, name='dashboard'),

]
