from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import FriendRequest, FriendList, BlackList
from django.contrib.auth.models import User


def handle_add_friend(request, user_id):
	FriendsList.objects.create(user_id=request.user.id, friend_id=user_id)


def handle_delete_friend(request, user_id):
	FriendsList.objects.get(friend_id=user_id, user_id=request.user.id).delete()


def handle_accept_friend(request, friend_id):
	accept_friend = get_object_or_404(FriendsList, user_id=friend_id, friend_id=request.user)

	if not accept_friend.is_friend:
		accept_friend.is_friend = True
		accept_friend.save()
		messages.success(request, 'Friend accepted')


def handle_decline_friend(request, friend_id):
	decline_friend = get_object_or_404(FriendsList, user_id=friend_id, friend_id=request.user)

	if decline_friend.is_friend:
		decline_friend.delete()
		messages.info(request, "Friend request declined.")


@login_required(login_url='/login/')
def friends_list_view(request):
	# get all the user's id who want to befriend the current authorized user and who aren't friend with the user yet
	friend_ids = FriendsList.objects.values_list('user_id', flat=True).filter(friend_id=request.user, is_friend=False)
	# get all the user's objects based on a filter -> friend_ids
	friend_requests = User.objects.filter(id__in=friend_ids)

	if request.method == 'POST':
		friend_id = request.POST.get('user_id', None)

		if "accept_friend" in request.POST:
			handle_accept_friend(request, friend_id)

		elif "decline_friend" in request.POST:
			handle_decline_friend(request, friend_id)

		return redirect('friends')

	return render(request, 'socials/friends.html', {'friend_requests': friend_requests})
