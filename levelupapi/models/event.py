from django.db import models

class Event(models.Model):
    """django event instance"""
    description = models.CharField(max_length=150)
    date = models.DateField(auto_now=False, auto_now_add=False)
    time = models.TimeField()
    organizer = models.ForeignKey('Gamer', on_delete=models.CASCADE, related_name='events')
    attendees = models.ManyToManyField('Gamer', related_name='attending')
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='events')
    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value