from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
import datetime
from django.utils import timezone
from Interface import Interface
from .models import HuntUser, HuntCommand, Penalty, Game, Landmark

def index(request):
    try:
        Landmark.objects.get(name="dummy")
    except Landmark.DoesNotExist:
        landmark = Landmark(name="dummy", clue="dummy", question="dummy", answer="dummy", order_num=-1)
        landmark.save()
    try:
        HuntUser.objects.get(name="maker")
    except HuntUser.DoesNotExist:
        maker = HuntUser(name="maker", password="password", current_landmark=landmark)
        maker.save()
    # try:
    #    Penalty.objects.get(name="time")
    # except Penalty.DoesNotExist:
    #    penalty = Penalty(name="time", value=30)
    #    penalty.save()
    # try:
    #     Penalty.objects.get(name="guesses")
    # except Penalty.DoesNotExist:
    #    penalty = Penalty(name="guesses", value=3)
    #    penalty.save()
    try:
        Game.objects.get(name="game")
    except Game.DoesNotExist:
        game = Game(name="game", running=False, time_start=timezone.now())
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
        teams = HuntUser.objects.exclude(name="maker")
        context = {"huntUser": request.POST["huntUser"],"teams": teams,
                   "landmarks": Landmark.objects.exclude(name="dummy"),
                   "running": Game.objects.get(name="game").running}
        if u.name == "maker":
            return render(request,"gamemaker.html",context)
        else:
            return render(request,"team.html",context)
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

def addlandmark(request):
    command = request.POST["command"] + " " + request.POST["landmarkName"] + ", " + \
        request.POST["landmarkClue"] + ", " + request.POST["landmarkQuestion"] + \
        ", " + request.POST["landmarkAnswer"]
    return command

def creategame(request):
    landmarks = request.POST.getlist("landmarkName")
    command = request.POST["command"]
    first = True
    for landmark in landmarks:
        if landmark:
            if first:
                command = command + " " + landmark
                first = False
            else:
                command = command + ", " + landmark

    return command

def gamemaker(request):
    switch = {
        "addlandmark": lambda request: addlandmark(request),
        "creategame": lambda request: creategame(request)
    }
    command = switch[request.POST["command"]](request)
    i = Interface.Interface()
    u = HuntUser.objects.get(name=request.POST["huntUser"])
    c = HuntCommand(text=command, user=u, timestamp=timezone.now())
    c.save()
    i.process(command, request.POST["huntUser"])
    context = {"huntUser": request.POST["huntUser"], "landmarks": Landmark.objects.exclude(name="dummy"),
               "teams": HuntUser.objects.exclude(name="maker"), "running": Game.objects.get(name="game").running}
    return render(request, "gamemaker.html", context)

def toggle_game(request):
    game = Game.objects.get(name="game")
    game.running = not game.running
    game.time_start = datetime.datetime.now(tz=timezone.utc)
    game.save()
    context = {"huntUser": request.POST["huntUser"], "landmarks": Landmark.objects.exclude(name="dummy"),
               "teams": HuntUser.objects.exclude(name="maker"), "running": game.running}
    return render(request, "gamemaker.html", context)

def team(request):
    return render(request, "team.html")