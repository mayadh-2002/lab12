from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # أنشئ مستخدم جديد
        user = User.objects.create_user(username=username, password=password)
        login(request, user)  # سجله مباشرة إذا تحب
        return redirect('/users/login')  # أو أي صفحة بعد التسجيل
    return render(request, 'users/register.html')

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = User.objects.create_user(username=username, password=password)
        messages.success(request, "Account created successfully. You can now log in.")
        return redirect('/users/login')
    return render(request, "users/register.html")
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('/users/login')  # أو إلى الصفحة الرئيسية "/"
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in ✅")
            return redirect("/books/list_books/")
        else:
            messages.error(request, "❌ Invalid username or password")
    return render(request, "users/login.html")