from django.contrib.staticfiles.storage import staticfiles_storage

from .forms import LoginForm

def common_variables(request):
    skin = request.session.get("skin", "light")
    return {
        'user': request.user,
        'skin': skin,
        'skin_css_url': staticfiles_storage.url("skins/%(skin)s/main.css" % {'skin': skin}),
        'skin_favico_url': staticfiles_storage.url("skins/%(skin)s/img/drak.svg" % {'skin': skin}),
        'skin_logo_url': staticfiles_storage.url("skins/%s/img/logo.gif" % skin),
        'login_form': LoginForm()
    }
