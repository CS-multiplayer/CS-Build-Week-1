import random 
from django.contrib.auth.models import User
from adventure.models import Room, Player


Room.objects.all().delete()

r = Room()
# r.testFunc()
w = World()
num_rooms = 115
width = 15
height = 15
w.generate_rooms(width, height, num_rooms)

newRooms = []
def rooms():
    newRooms.append(r.__repr__())

rooms()

print(newRooms)

players = Player.objects.all()
for p in players:
    p.current_rooms = w.grid[0][0].id
    p.save()
