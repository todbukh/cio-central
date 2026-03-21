from django.db import models
from core.models import User

class Channel(models.Model):
    # TODO: add logic to displaying appropriate error message in forms when a channel name is taken
    name = models.CharField(max_length=30, unique=True)
    exec_only = models.BooleanField()
    builtin = models.BooleanField(default=False)  # this marks if the channel is a 'built-in' channel that can't be deleted/modified


class Message(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=2000)
    sent_at = models.DateTimeField(auto_now=True)

    def timestamp(self):
        return self.sent_at.strftime("%m/%d/%Y %I:%M%p")