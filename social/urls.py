from django.urls import path
from social.views import friends_list_view

urlpatterns = [
	path('friends/', friends_list_view, name='friends'),
]
