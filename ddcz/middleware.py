def attach_profile(get_response):
    def middleware(request):
        if request.user.is_authenticated:
            request.ddcz_profile = request.user.userprofile
        response = get_response(request)
        return response

    return middleware
