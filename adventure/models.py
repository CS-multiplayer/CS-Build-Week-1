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
    n_to = models.IntegerField(default=-1)
    s_to = models.IntegerField(default=-1)
    e_to = models.IntegerField(default=-1)
    w_to = models.IntegerField(default=-1)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)

    def __repr__(self):
        n_to = self.n_to
        s_to = self.s_to
        e_to = self.e_to
        w_to = self.w_to
        # , name:{self.name}, description:{self.description}, n_to:{n_to}, s_to:{s_to}, e_to:{e_to}, w_to:{w_to}, x:{self.x}, y:{self.y}"
        return f"{{id:{self.id}, n_to:{n_to}, s_to:{s_to}, e_to:{e_to}, w_to:{w_to}, x:{self.x}, y:{self.y}}}"

    def connect_rooms(self, destinationRoom, direction):
        destinationRoomID = destinationRoom.id
        try:
            destinationRoom = Room.objects.get(id=destinationRoomID)
        except Room.DoesNotExist:
            print("That room does not exist")
        else:
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


@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()
