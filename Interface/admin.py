from django.contrib import admin
from .models import HuntUser, HuntCommand, Landmark, Penalty

admin.site.register(HuntUser)
admin.site.register(HuntCommand)
admin.site.register(Landmark)
admin.site.register(Penalty)