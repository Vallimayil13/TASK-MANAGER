from django.shortcuts import render, redirect,get_object_or_404
from task.forms import SignupForm
from django.contrib.auth import authenticate, login , logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from task.models import Task
from task.forms import TaskForm
from django.db.models import Q
from django.utils import timezone

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()    
    return render(request, 'signup.html', {'form': form})

def user_login(request):  
    if request.method== 'POST':   
        username=request.POST['username']  
        password=request.POST['password']
        user = authenticate(username=username, password=password) 
        
        if user is not None:
            if user.is_active:   
                login(request, user)  
                return redirect('dashboard')  
            else:
                return HttpResponse("User account is disabled.")        
        else:
            return HttpResponse("Invalid username or password.")
       
    return render(request, "login.html",{})

@login_required(login_url="login")
def user_logout(request):
    logout(request)
    return redirect("login")


@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()

    return render(request, 'createTask.html', {
        'form': form,
        'title': 'Create Task',
        'button_text': 'Save'
    })

@login_required
def update_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'createTask.html', {
        'form': form,
        'title': 'Update Task',
        'button_text': 'Update'
    })



@login_required(login_url="login")
def task_list(request):
    
    tasks = Task.objects.filter(user=request.user)

    # Search by Title
    search_query = request.GET.get('search')
    if search_query:
        tasks = tasks.filter(title__icontains=search_query)

    # Filter by Status
    status_filter = request.GET.get('status')
    if status_filter:
        tasks = tasks.filter(status=status_filter)

    # Filter by Priority
    priority_filter = request.GET.get('priority')
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)

    return render(request, 'task_list.html', {'tasks': tasks})


@login_required(login_url="login")
def delete_task(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')

    
    return render(request, 'deleteTask.html', {'task': task})



@login_required(login_url="login")
def dashboard(request):
    user_tasks = Task.objects.filter(user=request.user)
    today = timezone.now().date()

    status = {
        'total': user_tasks.count(),
        'pending': user_tasks.filter(status='PENDING').count(),
        'completed': user_tasks.filter(status='DONE').count(),
        'overdue': user_tasks.filter(due_date__lt=today).exclude(status='DONE').count(),
    }

    return render(request, 'dashboard.html', {'status': status})
