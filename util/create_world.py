import random 
from django.contrib.auth.models import User
from adventure.models import Player
from adventure.models import Room

Room.objects.all().delete()

w = Room()
# num_rooms = 115
# width = 15
# height = 15
# w.generate_rooms(width, height, num_rooms)
# w.print_rooms()
w.testFunc()

players = Player.objects.all()
for p in players:
    p.currentRoom = w.grid[0].id
    p.save()
