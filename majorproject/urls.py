"""majorproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from majorapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.index,name="index"),
    path("about/",views.aboutpage,name="about"),
    path("contact/",views.contactpage,name="contact"),
    path("allproperties/",views.allpropertiespage,name="allproperties"),
    path("propertydetail/",views.propertydetailpage,name="propertydetail"),
    path("myproperties/",views.mypropertiespage,name="myproperties"),
    path("changepassword/",views.changepasswordpage,name="changepassword"),
    path("addproperty/",views.addpropertypage,name="addproperty"),
    path("category/",views.categorypage,name="category"),
    path('register/',views.register,name="register"),
    path('check_user/',views.check_user,name="check_user"),
    path('user_login/',views.user_login,name="user_login"),
    path('forget_pass/',views.forget_pass,name='forget_pass'),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('user_logout/',views.user_logout,name="user_logout"),
    path('edit_profile/',views.editprofile,name="editprofile"),
    path('addproperty/',views.addpropertypage,name="addproperty"),
    path('myproperty/',views.mypropertiespage,name="myproperty"),
    path('changepassword/',views.changepasswordpage,name="changepassword"),
    path('favourite/',views.favourite,name="favourite"),
    path('single_property/',views.single_property,name="single_property"),
    path('update_property/',views.update_property,name="update_property"),
    path('delete_property/',views.delete_property,name="delete_property"),
    path('all_properties/',views.all_properties,name="all_properties"),
    path('forget_pass/',views.forget_pass,name="forget_pass"),
    path('reset_pass/',views.reset_pass,name="reset_pass"),

    
]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
