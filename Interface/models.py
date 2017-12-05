from django.db import models

class Landmark(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=255)
    clue = models.CharField(max_length=255)
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    order_num = models.IntegerField(default=0)

class HuntUser(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    current_landmark = models.ForeignKey(Landmark)


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