from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import FriendsList
from django.contrib.auth.models import User


@login_required(login_url='/login/')
def friends_list_view(request):
	request_user_id = request.user
	friend_ids = FriendsList.objects.values_list('user_id', flat=True).filter(friend_id=request_user_id,
	                                                                          is_friend=False)
	friend_requests = User.objects.filter(id__in=friend_ids)

	if request.method == 'POST':
		friend_id = request.POST.get('user_id', None)
		if "accept_friend" in request.POST:
			friend_entry = get_object_or_404(FriendsList, user_id=friend_id, friend_id=request_user_id)
			if not friend_entry.is_friend:
				friend_entry.is_friend = True
				friend_entry.save()
				messages.success(request, 'Friend accepted')
			else:
				messages.warning(request, 'You already accepted')

		elif "decline_friend" in request.POST:
			declined_friend = FriendsList.objects.filter(user_id=friend_id, friend_id=request_user_id)
			if declined_friend.exists():
				declined_friend.delete()
				messages.info(request, "Friend request declined.")
			else:
				messages.warning(request, 'You already declined')

		return redirect('friends')

	return render(request, 'socials/friends.html', {'friend_requests': friend_requests})
