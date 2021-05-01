from django.shortcuts import render
from django.contrib.admin.views import decorators

from ddcz.models import LevelSystemParams


@decorators.staff_member_required()
def dashboard(request):

    return render(request, "dashboard.html", {})


@decorators.staff_member_required()
def levelsystem(request):
    """Allows users to configure how level system works"""
    params = LevelSystemParams.objects.all()

    return render(request, "levelsystem/view.html", {"level_params": params})
