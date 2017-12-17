from django.contrib import admin
from .models import HuntUser, HuntCommand, Landmark, Penalty, Game

admin.site.register(HuntUser)
admin.site.register(HuntCommand)
admin.site.register(Landmark)
admin.site.register(Penalty)
admin.site.register(Game)