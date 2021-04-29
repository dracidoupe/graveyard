def attach_profile(get_response):
    def middleware(request):
        if request.user.is_authenticated:
            request.ddcz_profile = request.user.userprofile
        else:
            request.ddcz_profile = None
        response = get_response(request)
        return response

    return middleware
