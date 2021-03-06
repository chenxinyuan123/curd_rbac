"""curd_rbac URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from curd import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login),
    url(r'^users/add/', views.user_add),
    url(r'^users/edit/(\d+)', views.user_edit),
    url(r'^users/delete/(\d+)', views.user_delete),
    url(r'^users/', views.user),
    url(r'^logout/', views.logout),
    url(r'^roles/add/', views.role_add),
    url(r'^roles/edit/(\d+)', views.role_edit),
    url(r'^roles/delete/(\d+)', views.role_delete),
    url(r'^roles/', views.role),
    url(r'^assets/', views.assets),
    url(r'^others/demo1/', views.user),
    url(r'^others/demo2/', views.role),
    url(r'^$', views.index),
]
