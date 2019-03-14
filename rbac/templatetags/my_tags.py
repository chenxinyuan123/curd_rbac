from django import template
register = template.Library()

@register.inclusion_tag("header.html")
def get_head(request):
    user = request.session.get("user")
    return {"user":user}

@register.inclusion_tag("menu_left.html")
def get_leftmenu(request):
    user = request.session.get("user")
    menuperm_list = request.session.get("menuperm_list")
    return {"user":user,"menuperm_list":menuperm_list}