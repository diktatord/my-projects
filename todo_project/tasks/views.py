from django.shortcuts import render, redirect, get_object_or_404
from .models import Task

def index(request):
    task = Task.objects.all()
    return render(request, 'tasks/index.html', {'tasks': task})

def view_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'tasks/view_task.html', {'tasks': task})

def create_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST.get('description', "")
        Task.objects.create(title=title, description=description)
        return redirect('index')
    return render(request, 'tasks/create_task.html')

def edit_task(request,task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.title = request.POST['title']
        task.description = request.POST.get('description',"")
        task.completed = 'completed' in request.POST
        task.save()
        return redirect('index')
    return render(request, 'tasks/edit_task.html', {'tasks': task})

def delete_task(request,task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('index')
    return render(request, 'tasks/delete_task.html', {'tasks': task})
