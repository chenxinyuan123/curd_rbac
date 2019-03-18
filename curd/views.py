from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
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

            #用户的权限注册到session中

            from rbac.service.permission import init_session
            init_session(request,user_obj)

            next_href = request.GET.get("next")
            print("next_href==========>", next_href)

            if next_href:
                return redirect(next_href)
            else:
                return redirect("/")

    return render(request,"login.html")

def index(request):
    user = request.session["user"]
    return render(request, "index2.html",locals())

class Per(object):
    def __init__(self,action):
        self.action = action
    def add(self):
        return "add" in self.action
    def delete(self):
        return "delete" in self.action
    def edit(self):
        return "edit" in self.action
    def list(self):
        return "list" in self.action

def user(request):

    users_obj = User.objects.all()
    roles_obj = Role.objects.all()

    for users in users_obj:
        roles = users.roles.all()
        ret = []
        for role in roles:
            ret.append(str(role))
        val = ", ".join(ret)
        users.r = val

    action = request.actions
    per = Per(action)


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
        isdelete = User.objects.filter(pk=pk).delete()
        # isdelete = User.objects.filter(pk=pk)
        # isdelete = ""
        if isdelete:
            data["status"]=1
        else:
            data["status"]=0
        print("data==========>",data)
    return JsonResponse(data)

def role_add(request):
    return HttpResponse("role_add")
def role(request):
    #role_obj = User.objects.all().values("roles__title","roles__permissions__title").distinct()
    role_obj = Role.objects.all()

    action = request.actions
    per = Per(action)
    for roles in role_obj:
        permis = roles.permissions.all()
        role_group = roles.permissions.all().values("group__title").distinct()
        ret = []
        for roleg in role_group:
            ret.append(roleg["group__title"])

        temp = []
        for perm in permis:
            temp.append(str(perm))
        roles.a = ",".join(temp)
        roles.role_group = ",".join(ret)

    return render(request,"roles.html",{"role_obj":role_obj})
def role_edit(request,pk):
    return HttpResponse("role_edit")
def role_delete(request,pk):
    return HttpResponse("role_delete")


def logout(request):
    del request.session["user"]
    del request.session["permissions_dict"]
    del request.session["menuperm_list"]
    return redirect("/login/")

def demo(request):
    return HttpResponse("This is demo page")

