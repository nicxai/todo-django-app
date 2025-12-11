from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from .forms import TaskForm, UserForm, MyUserCreationForm
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Task, User

# Create your views here.


def home(request):
    q = request.GET.get("q", "")
    if request.user.is_anonymous:
        tasks = []
    else:
        tasks = Task.objects.filter(user=request.user)

        if q:
            if q == "Completed":
                tasks = tasks.filter(completed=True)
            elif q == "Not-Completed":
                tasks = tasks.filter(completed=False)
            else:
                tasks = tasks.filter(priority=q)

        dones = str(tasks.filter(completed=True).count()) + " / " + str(tasks.count())

        context = {"tasks": tasks, "dones": dones}
        return render(request, "base/home.html", context)
        
    return render(request, "base/home.html", {})


def taskPage(request, pk):
    task = get_object_or_404(Task, id=pk)

    if request.user.id != task.user.id:
        return redirect("home")

    context = {"task": task}
    return render(request, "base/task.html", context)


@login_required(login_url="login")
def createTask(request):
    form = TaskForm()

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()

            return redirect("home")

    context = {
        "form": form,
    }
    return render(request, "base/create-task.html", context)


@login_required(login_url="login")
def deleteTask(request, pk):
    task = get_object_or_404(Task, id=pk)
    if request.user.id != task.user.id:
        return redirect("home")

    task.delete()
    return redirect("home")


@login_required(login_url="login")
def completeTask(request, pk):
    task = Task.objects.get(id=pk)

    if request.user.id != task.user.id:
        return redirect("home")

    task.completed = True
    task.save()

    return redirect("home")


def editTask(request, pk):
    task = get_object_or_404(Task, id=pk)
    form = TaskForm(instance=task)

    if request.user.id != task.user.id:
        return redirect("home")

    if request.method == "POST":
        task.name = request.POST.get("name")
        task.description = request.POST.get("description")
        task.priority = request.POST.get("priority")
        if request.POST.get("deadline") != '':
            task.deadline = request.POST.get("deadline")
        task.save()
        return redirect("home")

    context = {"form": form}
    return render(request, "base/create-task.html", context)


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == "POST":
        form = MyUserCreationForm(request.POST, request.FILES)

        if form.is_valid():

            username = form.cleaned_data["username"].lower()

            if not User.objects.filter(username=username).exists():
                user = form.save(commit=False)
                user.username = username
                user.save()

                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Username is Already Taken")

        else:
            messages.error(request, "An Error Occured During Registration")

    context = {"page": "register", "form": form}
    return render(request, "base/login-register.html", context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        try:
            User.objects.get(username=username)
        except:
            messages.error(request, "User Does not Exist")

            context = {"page": "login"}
            return render(request, "base/login-register.html", context)

        user = authenticate(request, username=username, password=password)

        if user == None and messages:
            messages.error(request, "Wrong Password")
        else:
            login(request, user)
            return redirect("home")

    context = {"page": "login"}
    return render(request, "base/login-register.html", context)


def logoutPage(request):
    logout(request)
    return redirect("home")
