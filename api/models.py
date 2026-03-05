from django.db import models


class WorldState(models.Model):

    room_id = models.CharField(max_length=100, unique=True)

    boss_hp = models.IntegerField(default=120)

    fase = models.IntegerField(default=1)

    entropia = models.FloatField(default=0)

    memoria = models.JSONField(default=list)

    updated_at = models.DateTimeField(auto_now=True)


class NPC(models.Model):

    npc_id=models.CharField(max_length=100)

    personalidade=models.CharField(max_length=100)

    humor=models.FloatField(default=0)

    memoria=models.JSONField(default=list)
