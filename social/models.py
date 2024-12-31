from django.db import models
from django.contrib.auth.models import User


class FriendRequest(models.Model):
	from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_request')
	to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_request')
	sent_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('from_user', 'to_user')


class FriendList(models.Model):
	user1 = models.ForeignKey(User, on_delete=models.CASCADE)
	user2 = models.ForeignKey(User, on_delete=models.CASCADE)
	befriended_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('user1', 'user2')


class BlackList(models.Model):
	blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_user')
	blocked = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocker')
	blocked_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('blocker', 'blocked')
