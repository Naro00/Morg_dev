from django.db import models
from core import models as core_models

class Conversation(core_models.TimeStampModel):
    """Conversation model definition"""

    participants = models.ManyToManyField(
        "users.User", related_name="conversation", blank=True
    )

    def __str__(self):
        username = []
        for user in self.participants.all():
            username.append(user.username)
        return ", ".join(username)

    def count_messages(self):
        return self.message.count()
    count_messages.short_description = "Number of Messages"

    def count_participants(self):
        return self.participants.count()
    count_participants.short_description = "Number of Participants"

class Message(core_models.TimeStampModel):
    """Message model definition"""

    Message = models.TextField()
    user = models.ForeignKey(
        "users.User", related_name="massages",  on_delete=models.CASCADE)
    conversations = models.ForeignKey(
        "Conversation", related_name="massages",  on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user} says: {self.Message}"