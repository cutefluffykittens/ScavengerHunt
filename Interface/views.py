from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
import datetime
from django.utils import timezone
from Interface import Interface
from .models import HuntUser, HuntCommand, Penalty, Game


def index(request):
    try:
        HuntUser.objects.get(name="maker")
    except HuntUser.DoesNotExist:
        maker = HuntUser(name="maker", password="password")
        maker.save()
    try:
        Penalty.objects.get(name="time")
    except Penalty.DoesNotExist:
        penalty = Penalty(name="time", value=30)
        penalty.save()
    try:
        Penalty.objects.get(name="guesses")
    except Penalty.DoesNotExist:
        penalty = Penalty(name="guesses", value=3)
        penalty.save()
    try:
        Game.objects.get(name="game")
    except Game.DoesNotExist:
        game = Game(name="game", running=False)
        game.save()
    return render(request, 'index.html', {"message":""})

def validate(request):

    message = "XXX"
    try:
        u = HuntUser.objects.get(name=request.POST["huntUser"])
    except HuntUser.DoesNotExist:
        message = "No user named " + request.POST["huntUser"]
    else:
        if u.password != request.POST["password"]:
            message = "Invalid password"
    if message == "XXX":
        context = {"huntUser": request.POST["huntUser"]}
        return render(request,"terminal.html",context)
    else:
        return render(request,"index.html",{"message":message})


def terminal(request):
    i = Interface.Interface()
    u = HuntUser.objects.get(name=request.POST["huntUser"])
    c = HuntCommand(text=request.POST["command"],user=u,timestamp=timezone.now())
    c.save()
    if request.POST["command"] == "logout":
        return render(request, "index.html")
    output = i.process(request.POST["command"], request.POST["huntUser"])
    context = {"huntUser":request.POST["huntUser"],"output":output}
    return render(request, "terminal.html", context)

