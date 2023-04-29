from django.contrib.auth import authenticate, login
from django.http import HttpRequest
from django.shortcuts import render, redirect


# Create your views here.

def login_view(req: HttpRequest):
    print(req.user)
    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']
        print(username)
        print(password)

        user = authenticate(req, username=username, password=password)
        login(req, user)

        print(user)
        # if user is not None:
        #     login(req, user)
        #     return redirect(home_index)

    return render(req, "login.html")
