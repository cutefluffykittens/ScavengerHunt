from django.db import models
from django.utils import timezone
from datetime import datetime


class Landmark(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=255)
    clue = models.CharField(max_length=255)
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    order_num = models.IntegerField(default=0)
    points = models.IntegerField(default=10)


class HuntUser(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    current_landmark = models.ForeignKey(Landmark)
    penalties = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    question_requested = models.BooleanField(default=False)
    time_requested = models.DateTimeField(default=timezone.now)
    guesses = models.IntegerField(default=0)
    game_ended = models.BooleanField(default=False)


class HuntCommand(models.Model):
    def __str__(self):
        return self.text
    text = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    user = models.ForeignKey(HuntUser)


class Penalty(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=255)
    value = models.IntegerField()


class Game(models.Model):
    name = models.CharField(max_length=255, default="game")
    running = models.BooleanField(default=False)
    time_start = models.DateTimeField(default=timezone.now)
    game_period = models.IntegerField(default=60)
    guess_period = models.IntegerField(default=5)   # default = 5 minutes
    num_guesses = models.IntegerField(default=5)
    time_penalty = models.IntegerField(default=5)
    guess_penalty = models.IntegerField(default=5)
    last_landmark_bonus = models.IntegerField(default=50)
