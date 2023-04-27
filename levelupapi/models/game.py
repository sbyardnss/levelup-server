from django.db import models

class Game(models.Model):
    """game django instance"""
    title = models.CharField(max_length=50)
    number_of_players = models.IntegerField()
    maker = models.CharField(max_length=50)
    skill_level = models.IntegerField()
    type = models.ForeignKey('Gametype', on_delete=models.CASCADE, related_name='games')
    gamer = models.ForeignKey('Gamer', on_delete=models.CASCADE, related_name='games')
