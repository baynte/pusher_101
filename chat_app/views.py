from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from pusher import Pusher
from .models import *
from .forms import RegisterForm
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.views import View
from django.http import JsonResponse
from django.views.decorators.http import require_POST

pusher = Pusher(
    app_id=settings.PUSHER_APP_ID,
    key=settings.PUSHER_APP_KEY,
    secret=settings.PUSHER_APP_SECRET,
    cluster=settings.PUSHER_APP_CLUSTER
)

@login_required(login_url='login/')
def index(request):
    context = {
        'PUSHER_APP_KEY': settings.PUSHER_APP_KEY,
        'PUSHER_APP_CLUSTER': settings.PUSHER_APP_CLUSTER,
    }
    return render(request, "chat.html", context);

@csrf_exempt
def broadcast(request):
    message = Conversation(message=request.POST.get('message', ''), status=Conversation.DELIVERED, user=request.user);
    message.save();
    
    message = {'name': message.user.username, 'status': message.status, 'message': message.message, 'id': message.id, 'event_type': 'broadcast'}
    
    pusher.trigger(u'a_channel', u'an_event', message)
    return JsonResponse(message, safe=False)

def conversations(request):
    data = Conversation.objects.all()
    data = [{'name': person.user.username, 'status': person.status, 'message': person.message, 'id': person.id} for person in data]
    return JsonResponse(data, safe=False)

@csrf_exempt
def delivered(request, id):
    message = Conversation.objects.get(pk=id);

    if request.user.id != message.user.id:
        socket_id = request.POST.get('socket_id', '')
        message.status = Conversation.RECEIVED;
        message.save();
        message = {'name': message.user.username, 'status': message.status, 'message': message.message, 'id': message.id, 'event_type': 'delivered'}
        pusher.trigger(u'a_channel', u'delivered_message', message, socket_id)
        return HttpResponse('ok');
    else:
        return HttpResponse('Awaiting Delivery');


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            messages.success(request, 'Registration successful!')
            return redirect('index')
        return render(request, 'register.html', {'form': form})

@require_POST
def edit_message(request, message_id):
    message = Conversation.objects.get(pk=message_id)
    if request.user == message.user:
        message.message = request.POST.get('message')
        message.save()

        message = {'name': message.user.username, 'status': message.status, 'message': message.message, 'id': message.id, 'event_type': 'edit'}
        pusher.trigger(u'a_channel', u'an_event', message)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=403)

@require_POST
def delete_message(request, message_id):
    message = Conversation.objects.get(pk=message_id)
    if request.user == message.user:
        message.delete()
        message = {'name': message.user.username, 'status': message.status, 'message': message.message, 'id': message.id, 'event_type': 'delete'}
        pusher.trigger(u'a_channel', u'an_event', message)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=403)
