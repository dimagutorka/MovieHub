from django.urls import path
from users.views import registration_view, login_view, logout_view, user_profile_view


urlpatterns = [
	path('registration/', registration_view, name='registration'),
	path('login/', login_view, name='login'),
	path('logout/', logout_view, name='logout'),
	path('profile/<int:user_id>', user_profile_view, name='profile'),

]