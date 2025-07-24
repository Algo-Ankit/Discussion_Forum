# take our python objects and convert them to JSON  # this is a serializer
from rest_framework.serializers import ModelSerializer
from base.models import Room

class RoomSerializer(ModelSerializer):  #same to room form
    class Meta:
        model = Room
        fields = '__all__' # this means that we want to serialize all the fields in the model