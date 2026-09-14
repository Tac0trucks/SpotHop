from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required
def home_view(request):
    mock_spots = [
        {"name": "Campus Brew Co.", "wifi": "85 Mbps", "outlets": "Plentiful", "noise": "Quiet", "price": "₱₱"},
        {"name": "Library 3rd Floor Hub", "wifi": "120 Mbps", "outlets": "Scarce", "noise": "Silent", "price": "Free"},
        {"name": "Common Grounds Café", "wifi": "45 Mbps", "outlets": "Plentiful", "noise": "Moderate", "price": "₱"},
    ]
    return render(request, "home/home.html", {"spots": mock_spots})

def logout_view(request):
    logout(request)
    return redirect("login:login")