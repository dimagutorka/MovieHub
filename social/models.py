from django.db import models
from django.contrib.auth.models import User


class FriendsList(models.Model):
	FRIEND_STATUS_CHOICES = {
		'NF': 'Not Friend',
		'F': 'Friend',
		'B': 'Blocked',
		'P': 'Pending',
	}

	outgoing_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='outgoing')
	incoming_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incoming')
	is_friend = models.BooleanField(default=False)
	added_at = models.DateTimeField(auto_now=True)
	friendship = models.TextField(blank=False, null=False,
	                              choices=FRIEND_STATUS_CHOICES, default=FRIEND_STATUS_CHOICES['NF'])

	class Meta:
		unique_together = ('outgoing_user', 'incoming_user')

# Given a model instance, the display value for a field with choices can be accessed using the get_FOO_display()
# p.get_shirt_size_display() Large