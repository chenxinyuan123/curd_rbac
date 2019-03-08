from django.shortcuts import render,redirect
from rbac.models import *
from django.forms import ModelForm

# Create your views here.

class UserAdd(ModelForm):
    class Meta:
        model = User
        fields = "__all__"

        error_messages = {
            'name': {'required': "用户名不能为空"},
            'pwd': {'required': "密码不能为空"},
            'roles': {'required': "密码不能为空"},
        }

        from django.forms import widgets as wid
        widgets = {
            "name": wid.TextInput(attrs={"class": "form-control"}),
            "pwd": wid.TextInput(attrs={"class": "form-control"}),
            "roles": wid.SelectMultiple(attrs={"class": "form-control"})
        }

        labels = {
            "name": "用户名",
            "pwd": "密码",
            "roles": "角色",
        }

def login(request):

    if request.method == "POST":
        user = request.POST.get("username")
        pwd = request.POST.get("password")

        user_obj = User.objects.filter(name=user,pwd=pwd).first()
        if user_obj:
            request.session["user"] = user
            return redirect('/')

    return render(request,"login.html")

def index(request):
    user = request.session["user"]
    return render(request, "index2.html",locals())

def user(request):

    users_obj = User.objects.all()

    return render(request,"users.html",locals())

def user_add(request):
    useradd = UserAdd()
    if request.method=="POST":
        useradd = UserAdd(request.POST)
        if useradd.is_valid():
            useradd.save()
            return redirect('/users/')

    return render(request,"user_add.html",locals())

def user_edit(request,pk):
    obj = User.objects.filter(pk=pk).first()
    useradd = UserAdd(instance=obj)
    if request.method == "POST":
        useradd = UserAdd(request.POST,instance=obj)
        if useradd.is_valid():
            useradd.save()
            return redirect("/users/")
    return render(request, "user_add.html", locals())

def user_delete(request,pk):
    if request.method == "POST":
        print("pk=========>",pk)
        data = {}
        User.objects.filter(pk=pk).delete()
        # isdelete = User.objects.filter(pk=pk)
        isdelete = ""
        if isdelete:
            data["status"]=0
        else:
            data["status"]=1
        print("data==========>",data)
    return render(request, "user_add.html", {"data":data})

