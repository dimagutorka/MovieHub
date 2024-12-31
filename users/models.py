from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie, Genre


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	about_me = models.TextField(max_length=500, blank=True)
	birth_date = models.DateField(null=True, blank=True)
	photo = models.ImageField(upload_to='avatars/', blank=True, null=True)
	age = models.PositiveIntegerField(null=True, blank=True)
	favorite_movies = models.ManyToManyField(Movie, blank=True, related_name='favorite_movies')
	favorite_genres = models.ManyToManyField(Genre, blank=True, related_name='favorite_genres')

	def __str__(self):
		return self.user.username
