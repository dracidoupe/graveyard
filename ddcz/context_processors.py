from django.contrib.staticfiles.storage import staticfiles_storage

def common_variables(request):
    skin = request.session.get("skin", "light")
    return {
        'skin': skin,
        'skin_css_url': staticfiles_storage.url("skins/%(skin)s/main.css" % {'skin': skin}),
        'skin_logo_url': staticfiles_storage.url("skins/%s/img/logo.gif" % skin),
    }
