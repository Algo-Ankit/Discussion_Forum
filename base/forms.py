from django.forms import ModelForm
from .models import Room , User
from django.contrib.auth.forms import UserCreationForm

class myUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['avatar' , 'name' , 'username' , 'email' , 'bio' ,'password1' , 'password2']



class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        exclude = ['host' , 'participants']  # to exclude the host field from the form

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar' , 'name' , 'username' , 'email' , 'bio' ,'password']
