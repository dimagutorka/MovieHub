from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
	name = models.CharField(max_length=20, unique=True, db_index=True)

	def __str__(self):
		return self.name


class Movie(models.Model):
	title = models.CharField(max_length=100, db_index=True)
	overview = models.TextField(max_length=500, blank=True)
	release_date = models.DateField(null=True, blank=True)
	country = models.CharField(max_length=100)
	genre = models.ManyToManyField(Genre, related_name='movies')
	poster = models.ImageField(upload_to='movie_posters/',default='movie_posters/default-poster.jpg')
	adult = models.BooleanField(default=False)
	average_rating = models.FloatField(default=0.0)

	def __str__(self):
		return self.title

	class Meta:
		indexes = [
			models.Index(fields=['title', 'release_date', 'country', 'poster', 'average_rating']),
		]


class WatchLater(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watch_later')
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
	added_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('user', 'movie')


class MoviePlayList(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movie_playlist')
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
	name = models.CharField(max_length=100, unique=True)
	like = models.PositiveIntegerField(default=0)
	dislike = models.PositiveIntegerField(default=0)

	class Meta:
		unique_together = ('user', 'movie')

	# TODO-11: Create manager for most used filter-query

	"""
	1. Three categories of preferences:
	- not authorized
	- authorized but users are not friends
	- authorized and users are friends
	"""

