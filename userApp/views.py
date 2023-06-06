from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# Create your views here.

def user_login(req: HttpRequest):
    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']

        user = authenticate(req, username=username, password=password)
        if user is not None:
            login(req, user)
            return redirect("patient_list")
    return render(req, "login.html")


@login_required()
def user_logout(req: HttpRequest):
    logout(req)
    return redirect("user_login")
