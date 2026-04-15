from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def login_view(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/dashboard/')

        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return render(request, 'register.html', {'error': 'Username already exists'})
            else:
                User.objects.create_user(username=username, email=email, password=password1)
                return redirect('/')
        else:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

    return render(request, 'register.html')


# DASHBOARD
def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('/')
    return render(request, 'dashboard.html')


# LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')