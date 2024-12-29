from django.db import models
from django.contrib.auth.models import User


class FriendRequest(models.Model):
	from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_request')
	to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_request')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('from_user', 'to_user')


class FriendList(models.Model):
	user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships1')
	user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships2')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('user1', 'user2')


class BlackList(models.Model):
	blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_users')
	blocked = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blockers')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('blocker', 'blocked')
