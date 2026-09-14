from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserSettings

@login_required
def settings_view(request):
    settings, _ = UserSettings.objects.get_or_create(user=request.user)
    if request.method == "POST":
        settings.dark_mode = "dark_mode" in request.POST
        settings.email_notifications = "email_notifications" in request.POST
        settings.save()
        return redirect("user_settings:user_settings")
    return render(request, "user_settings/user_settings.html", {"settings": settings})