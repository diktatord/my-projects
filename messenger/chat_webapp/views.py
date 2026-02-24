from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Message
from .forms import UserForm, MessageForm

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            request.session['user_id'] = user.id
            return redirect('chat')
    else:
        form = UserForm()

    return render(request, 'chat_webapp/register.html', {'form': form})

def chat(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('register')

    user = User.objects.get(id=user_id)
    messages = Message.objects.all().order_by('timestamp')

    if request.method == 'POST':

        if 'edit_message_id' in request.POST:
            message_id = request.POST['edit_message_id']
            message = Message.objects.get(id=message_id)
            if message.user == user:
                form = MessageForm(request.POST, instance=message)
                if form.is_valid():
                    form.save()
                    return redirect('chat')

        elif 'delete_message' in request.POST:
            message_id = request.POST['delete_message']
            message = get_object_or_404(Message, id=message_id)
            if message.user == user:
                message.delete()
                return redirect('chat')


        else:
            form = MessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.user = user
                message.save()
                return redirect('chat')
    else:
        form = MessageForm()

    return render(request, 'chat_webapp/chat.html', {
        'form': form,
        'messages': messages,
        'user': user
    })
