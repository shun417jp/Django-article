from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from accounts.forms import ProfileForm
from .models import Profile

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # ユーザー作成後にProfileも作成
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('edit_profile')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})



@login_required
def profile_create(request):
    if hasattr(request.user, 'profile'):
        return redirect('profile_detail', username=request.user.username)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile_detail', username=request.user.username)
    else:
        form = ProfileForm()
    return render(request, 'blog/profile_create.html', {'form': form})

