from django.contrib.staticfiles.storage import staticfiles_storage

def common_variables(request):
    return {
        'skin': 'light',
        'skin_css_url': staticfiles_storage.url("skins/light/light.css"),
        'skin_logo_url': staticfiles_storage.url("skins/light/img/logo.gif"),
    }
