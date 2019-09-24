from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid
import random

class Room(models.Model):
    title = models.CharField(max_length=50, default="DEFAULT TITLE")
    description = models.CharField(
        max_length=500, default="DEFAULT DESCRIPTION")
    n_to = models.IntegerField(default= -1)
    s_to = models.IntegerField(default= -1)
    e_to = models.IntegerField(default= -1)
    w_to = models.IntegerField(default= -1)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    grid = None
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)

    def __repr__(self):
        n_to = self.n_to
        s_to = self.s_to
        e_to = self.e_to
        w_to = self.w_to
        # if n_to:
        #     n_to = self.n_to.id
        # if s_to:
        #     s_to = self.s_to.id
        # if e_to:
        #     e_to = self.e_to.id
        # if w_to:
        #     w_to = self.w_to.id

        return f"id:{self.id}, name:{self.name}, description:{self.description}, n_to:{n_to}, s_to:{s_to}, e_to:{e_to}, w_to:{w_to}, x:{self.x}, y:{self.y}"

    def generate_rooms(self, size_x, size_y, num_rooms):
        # Initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range(len(self.grid)):
            self.grid[i] = [None] * size_x

        # Start from lower-left corner (0,0)
        x = -1  # (this will become 0 on the first step)
        y = 0
        room_count = 0

        # Start generating rooms to the east
        direction = 1  # 1: east, -1: west
        horDirection = 1  # 1: up, -1: down

        # Generated Room Names
        roomAdj = ["Dark", "Old", "Old, Intact", "Loathsome", "Horrid",
                   "Empty", "Moist, Murky", "Suspicous", "Damp", "Gloomy", "Secret", "Filthy", "Misty", "Moldy", "Pestilent", "Cozy Little", "Dim", "Smokey", "Vacant", "Ancient"]
        roomNames = ["Cellar", "Cave", "Cabin", "Hideout",
                     "Pathway", "Corridor", "Cave", "Hideout",
                     "Pathway", "Corridor", "Treasure Room"]

        # Generated Room Descriptions
        descStarters = [
            "You approach a(n)", "You step forward and see a(n)", "You walk into a(n)", "This is a", "You creep into a(n)"]
        descInfo = ["It seems to give off an errie mood", "Its a pretty dark room, better watch you step!", "You see a sparkling light deeper in the dungeon, is it your imagination?",
                    "A terrible smell creeps up your nose.", "Seems like a cozy place", "Its a very quiet room. Too quiet.", "Its very dark in here.", "Dont be fooled.", "You hear some rocks hit the ground, better watch your step."]
        # While there are rooms to be created...
        previous_room = None
        while room_count < num_rooms:
            # Calculate the direction of the room to be created
            nextDi = random.randint(0, 18)
            canDown = horDirection <= 0
            canUp = horDirection >= 0

            if nextDi > 11 and canDown and not self.grid[y-1][x] and y > 1 and x < size_x - 2 and x > 1:
                room_direction = "s"
                horDirection = -1
                y -= 1
            elif x > 1 and nextDi > 16 and canUp:
                room_direction = "n"
                horDirection = 1
                y += 1
            elif direction > 0 and x < size_x - 1 and not self.grid[y][x+1]:
                room_direction = "e"
                horDirection = 0

                x += 1
            elif direction < 0 and x > 0 and not self.grid[y][x-1]:
                horDirection = 0
                room_direction = "w"
                x -= 1
            else:
                # If we hit a wall, turn north and reverse direction
                # If theres a room above it, go to the room above that
                if self.grid[y+1][x]:
                    while self.grid[y+1][x]:
                        y += 1
                        previous_room = self.grid[y][x]
                y += 1
                room_direction = "n"
                horDirection = 1
                direction *= -1

            currName = random.choice(roomAdj) + " " + random.choice(roomNames)
            roomDescription = random.choice(
                descStarters) + " " + currName.lower() + ". " + random.choice(descInfo)

            # print(horDirction)
            # Create a room in the given direction
            room = Room( title=currName,
                        description=roomDescription, x=x,y=y)
            # Note that in Django, you'll need to save the room after you create it

            # Save the room in the World grid
            self.grid[y][x] = room
            # print(self.grid[y][x].description)

            # Connect the new room to the previous room
            if previous_room is not None:
                previous_room.connect_rooms(room, room_direction)
            if nextDi < 10 and y > 0 and self.grid[y-1][x]:
                room.connect_rooms(self.grid[y-1][x], "s")
            # elif nextDi < 5 and self.grid[y][x+1]:
            #     room.connect_rooms(self.grid[y][x+1], "e")
            # Update iteration variables
            previous_room = room
            room_count += 1

    def connect_rooms(self, destinationRoom, direction):
        destinationRoomID = destinationRoom.id
        try:
            destinationRoom = Room.objects.get(id=destinationRoomID)
        except Room.DoesNotExist:
            print("That room does not exist")
        else:
            reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
            reverse_dir = reverse_dirs[direction]
            if direction == "n":
                self.n_to = destinationRoomID
                destinationRoom.s_to = self.id
            elif direction == "s":
                self.s_to = destinationRoomID
                destinationRoom.n_to = self.id
            elif direction == "e":
                self.e_to = destinationRoomID
                destinationRoom.w_to = self.id
            elif direction == "w":
                self.w_to = destinationRoomID
                destinationRoom.e_to = self.id
            else:
                print("Invalid direction")
                return
            self.save()

    def playerNames(self, currentPlayerID):
        return [p.user.username for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]

    def playerUUIDs(self, currentPlayerID):
        return [p.uuid for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]

    def testFunc(self):
        print('this is the Test')

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentRoom = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def initialize(self):
        if self.currentRoom == 0:
            self.currentRoom = Room.objects.first().id
            self.save()

    def room(self):
        try:
            return Room.objects.get(id=self.currentRoom)
        except Room.DoesNotExist:
            self.initialize()
            return self.room()


class World(models.Model):
    
    def print_rooms(self):
        '''
        Print the rooms in room_grid in ascii characters.
        '''
        # print(self.grid[0][0].name, self.grid[0][0].description)
        # Add top border
        str = "# " * ((3 + self.width * 5) // 2) + "\n"

        # The console prints top to bottom but our array is arranged
        # bottom to top.
        #
        # We reverse it so it draws in the right direction.
        reverse_grid = list(self.grid)  # make a copy of the list
        reverse_grid.reverse()
        for row in reverse_grid:
            # PRINT NORTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            # PRINT ROOM ROW
            str += "#"
            for room in row:
                if room is not None and room.w_to is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None:
                    str += f"{room.id}".zfill(3)
                else:
                    str += "   "
                if room is not None and room.e_to is not None:
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            # PRINT SOUTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"

        # Add bottom border
        str += "# " * ((3 + self.width * 5) // 2) + "\n"

        # Print string
        print(str)


@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()
