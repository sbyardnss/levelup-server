from django.db import models

class Event(models.Model):
    """django event instance"""
    description = models.CharField(max_length=150)
    date = models.DateField()
    time = models.TimeField()
    organizer = models.ForeignKey('Gamer', on_delete=models.CASCADE, related_name='events')
    attendees = models.ManyToManyField('Gamer', related_name='attending')
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='events')