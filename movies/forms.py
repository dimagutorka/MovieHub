from django import forms
from .models import WatchLater, Movie


class AddToWatchLater(forms.ModelForm):
	class Meta:
		model = WatchLater
		fields = []


class MovieForm(forms.ModelForm):
	class Meta:
		model = Movie
		fields = ['title', 'release_date', 'country', 'genres', 'poster']
