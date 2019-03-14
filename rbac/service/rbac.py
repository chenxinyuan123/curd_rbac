from django.utils.deprecation import MiddlewareMixin
import re
from django.shortcuts import HttpResponse,redirect

class rbac(MiddlewareMixin):
    def process_request(self, request):
        current_path = request.path_info

        valid_url_list = ["/login/","/logout/","/reg/","/admin/.*","/others/demo1","/others/demo2"]
        for valid_url in valid_url_list:
            ret = re.match(valid_url,current_path)
            if ret:
                return None

        #验证登陆状态:

        user_id = request.session.get("user")
        if not user_id:
            return redirect("/login/?next=%s"%(current_path))

        #检验权限
        permissions_dict = request.session.get("permissions_dict")

        print("permissions_dict===>",permissions_dict)
        for item in permissions_dict.values():
            urls = item['url']
            for reg in urls:
                reg="^%s$"%reg
                ret=re.match(reg,current_path)
                if ret:
                    request.actions=item['action']
                    return None
        return HttpResponse("没有访问权限!")

