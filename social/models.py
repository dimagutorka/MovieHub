from django.db import models
from django.contrib.auth.models import User


class FriendsList(models.Model):

	# FRIEND_STATIS_CHOICES = [
	# 	('not friends', ''),
	# 	('pending', ''),
	# 	('friends', '')
	# ]

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mainuser')
	friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
	is_friend = models.BooleanField(default=False)
	added_at = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = ('user', 'friend')


	#Given a model instance, the display value for a field with choices can be accessed using the get_FOO_display()
	# p.get_shirt_size_display() Large

	#Field help_text -  Extra “help” text to be displayed with the form widget. It’s useful for documentation even if your field isn’t used on a form.