from django.shortcuts import render , redirect
from django.db.models import Q
from django.contrib import messages 
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from .models import Room , Topic , Message , User 
from .forms import RoomForm , UserForm , myUserCreationForm
from django.http import HttpResponse



# Create your views here.
# we just add login page above all the views to make sure that the user is logged in before accessing the views

def loginPage(request):
    #dont use the name login as it is a reserved keyword (to avoid conflict .) -> built in function of django for logging in
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')
    # This is done to make sure that the user is not able to access the login page if he is already logged in


    if request.method == 'POST':
        email = request.POST.get('email').lower() # to make sure that the username/email is saved in lowercase
        password = request.POST.get('password')
        # to make sure that user exists
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')
            
        user = authenticate(request, email = email , password=password)
        
        if user is not None:
            login(request , user)
            return redirect('home')
        else:
            messages.error(request, 'Username and Password is incorrect or may not exist')
    
    context={'page':page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    # page='register'        ->  we dont actually need this as we are using page for login and register comes in else 
    form = myUserCreationForm()

    if request.method == 'POST':
        form = myUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # we use commit=False to make sure that the user is not saved in the database yet
            user.username = user.username.lower()  # to make sure that the username is saved in lowercase
            user.save()  # to save the user in the database  after changing the username to lowercase


            # login the user ny default after registration
            login(request , user)
            return redirect('home')

        else:
            messages.error(request, 'An error occured during registration')
            
    
    return render(request, 'base/login_register.html', {'form':form })





def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    # we use inline if statement to check if the query is not None  -> we check that if request method has something in it
    # if it is None then we set it to empty string


    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    # icontains is used to check to make sure whatever value we have in the topic name at least contains the value of q
    # we use __ to access the fields of the related model
    # i makes the search case insensitive        # __icontains is used to check if the value is present in the field
    # this is done for searching even if we write py in the search it will show all suggestions starting from py
    
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))[0:3]      # to show messages in the room | Q lookup method

    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages}
  
    return render(request, 'base/home.html', context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body') # name=body assigned in the form to send message
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)


    context={'room':room , 'room_messages':room_messages , 'participants':participants}
    return render(request, 'base/room.html' , context)

def profile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context={'user':user , 'rooms':rooms , 'room_messages':room_messages , 'topics':topics}
    return render(request, 'base/profile.html' , context)


@login_required(login_url='/login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)



@login_required(login_url='/login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)



@login_required(login_url='/login')
def deleteRoom(request , pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')


    if request.method == 'POST':
        room.delete()
        return redirect('home')


    return render(request, 'base/delete.html' , {'obj':room})


@login_required(login_url='/login')
def deleteMessage(request , pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!')


    if request.method == 'POST':
        message.delete()
        return redirect('home')


    return render(request, 'base/delete.html' , {'obj':message})

@login_required(login_url='/login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    
    if request.method == 'POST':
        form = UserForm(request.POST , request.FILES ,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile' , pk=user.id)



    
    return render(request, 'base/update-user.html', {'form': form})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q')!=None else ''
    # we use inline if statement to check if the query is not None  -> we check that if request method has something in it
    # if it is None then we set it to empty string
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html' , {'room_messages':room_messages})