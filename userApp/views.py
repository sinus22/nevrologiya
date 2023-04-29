from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest
from django.shortcuts import render, redirect


# Create your views here.

def user_login(req: HttpRequest):
    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']

        user = authenticate(req, username=username, password=password)
        if user is not None:
            print(user)
            login(req, user)
            return redirect("patient_list")
    return render(req, "login.html")


def user_logout(req: HttpRequest):
    logout(req)
    return redirect("user_login")
