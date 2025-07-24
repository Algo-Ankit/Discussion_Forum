from rest_framework.decorators import api_view
from rest_framework.response import Response
# from django.http import JsonResponse    # JsonResponse is a subclass of HttpResponse
from base.models import Room
from .serializers import RoomSerializer
from base.api import serializers

@api_view(['GET']) # this is a decorator that takes a list of allowed methods and here we are allowing only the GET method
def getroutes(request):
    # a view that shows us all the routes in our api
    routes = [
        'GET /api',
        'GET /api/rooms', # gives a json array of objects of all rooms in our database
        'GET /api/rooms/:id', # gives a json object of a room with the given id i.e. gives a single objectand info on a single room.

    ]
    return Response(routes ) #, safe=False)  # safe=False is used to allow serialization of objects other than dict (in this case a list) only for jsonresponse
# safe allows for the serialization of objects other than dict (in this case a list)
# safe means that it is allowed the list to be turned to json list
@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    # serialize the rooms
    serializer = RoomSerializer(rooms, many=True) # many=True means that we are serializing multiple objects here all from model.rooms
    return Response(serializer.data)

@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)