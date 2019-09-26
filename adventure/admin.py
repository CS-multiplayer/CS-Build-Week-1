from django.contrib import admin
from .models import Room, Player


class RoomAdmin(admin.ModelAdmin):
    pass


class PlayerAdmin(admin.ModelAdmin):
    pass


# Register your models here.
admin.site.register(Room, RoomAdmin)
admin.site.register(Player, PlayerAdmin)