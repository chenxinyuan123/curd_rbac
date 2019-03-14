from rbac.models import *
def init_session(request,user_obj):
    permissions = user_obj.roles.all().values("permissions__url","permissions__group_id","permissions__action","permissions__group__title" ).distinct()

    print("permissions====>",permissions)

    permissions_dict = {}
    menuperm_list = []
    for permission in permissions:
        url = permission["permissions__url"]
        groupid = permission["permissions__group_id"]
        action = permission["permissions__action"]
        title = permission["permissions__group__title"]
        if not groupid in permissions_dict:
            permissions_dict[groupid] = {
                "url" : [url],
                "action" : [action],
            }
        else:
            permissions_dict[groupid]["url"].append(url)
            permissions_dict[groupid]["action"].append(action)

        if action == "list":
            menuperm_list.append({"app":url.strip("/") ,"url":url,"title":title})


    # print("permissions_dict=======>",permissions_dict)
    # print("menuperm_dict======>",menuperm_list)
    request.session["permissions_dict"] = permissions_dict
    request.session["menuperm_list"] = menuperm_list


