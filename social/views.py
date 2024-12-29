from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .models import FriendRequest, FriendList, BlackList
from django.db.models import Q


def handle_send_friend_request(request, user_id):
	FriendRequest.objects.create(from_user=request.user.id, to_user=user_id)
	messages.success(request, 'Request to friends was sent successfully')


def handle_delete_friend(request, user_id):
	FriendList.objects.get(user1=request.user.id, user2=user_id).delete()
	FriendRequest.objects.get(from_user=request.user.id, to_user=user_id).delete()
	friend = get_object_or_404(User, pk=user_id)
	messages.success(request, f'You\'ve deleted user {friend.username} form your friend list')


def handle_accept_friend(request, friend_request_id):
	FriendList.objects.create(user1=request.user.id, user2=friend_request_id)
	messages.success(request, 'Friend accepted')


def handle_decline_friend(request, friend_request_id):
	FriendRequest.objects.get(from_user=request.user.id, to_user=friend_request_id).delete()
	messages.info(request, "Friend request declined.")


@login_required(login_url='/login/')
def friends_list_view(request):
	friendship = FriendList.objects.filter(Q(user1=request.user.id) | Q(user2=request.user.id))
	friends_list = [friend.user1 if friend.user2 == request.user.id else friend.user2 for friend in friendship]
	requests_friend_list = FriendRequest.objects.values_list('from_user', flat=True).filter(to_user=request.user.id)

	users = User.objects.filter(pk__in=requests_friend_list)

	if request.method == 'POST':
		friend_request_id = request.POST.get('friend_request_id', None)

		if "accept_friend" in request.POST:
			handle_accept_friend(request, friend_request_id)

		elif "decline_friend" in request.POST:
			handle_decline_friend(request, friend_request_id)

		return redirect('friends')

	return render(request, 'socials/friends.html',
	              {'friends_list': friends_list, 'requests_friend_list': requests_friend_list, 'users': users})
