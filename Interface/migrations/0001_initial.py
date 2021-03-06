# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-19 01:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='game', max_length=255)),
                ('running', models.BooleanField(default=False)),
                ('time_start', models.DateTimeField(default=django.utils.timezone.now)),
                ('game_period', models.IntegerField(default=60)),
                ('guess_period', models.IntegerField(default=5)),
                ('num_guesses', models.IntegerField(default=5)),
                ('time_penalty', models.IntegerField(default=5)),
                ('guess_penalty', models.IntegerField(default=5)),
                ('last_landmark_bonus', models.IntegerField(default=50)),
            ],
        ),
        migrations.CreateModel(
            name='HuntCommand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='HuntUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=20)),
                ('penalties', models.IntegerField(default=0)),
                ('score', models.IntegerField(default=0)),
                ('question_requested', models.BooleanField(default=False)),
                ('time_requested', models.DateTimeField(default=django.utils.timezone.now)),
                ('guesses', models.IntegerField(default=0)),
                ('game_ended', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Landmark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('clue', models.CharField(max_length=255)),
                ('question', models.CharField(max_length=255)),
                ('answer', models.CharField(max_length=255)),
                ('order_num', models.IntegerField(default=0)),
                ('points', models.IntegerField(default=10)),
            ],
        ),
        migrations.CreateModel(
            name='Penalty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('value', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='huntuser',
            name='current_landmark',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Interface.Landmark'),
        ),
        migrations.AddField(
            model_name='huntcommand',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Interface.HuntUser'),
        ),
    ]
