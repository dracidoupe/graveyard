from django.shortcuts import render
from django.contrib.admin.views import decorators


@decorators.staff_member_required()
def levelsystem(request):
    """ Allows users to configure how level system works """

    return render(request, 'levelsystem/view.html', {

    })