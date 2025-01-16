from sentry_sdk import set_user


def attach_profile(get_response):
    def middleware(request):
        if request.user.is_authenticated:
            request.ddcz_profile = request.user.userprofile
        else:
            request.ddcz_profile = None
        response = get_response(request)
        return response

    return middleware


def set_sentry_user_context(get_response):
    def middleware(request):
        if request.user.is_authenticated:
            set_user({"id": request.user.id, "username": request.ddcz_profile.nick})
        else:
            set_user(None)

        response = get_response(request)
        return response

    return middleware
