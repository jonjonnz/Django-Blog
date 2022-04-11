from django.contrib.auth import forms
from django.http import request
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth import login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

def signup_view(request):

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request,f'Account created for {user.get_username()}!')
            # login(request,user)

            return redirect('accounts:login')
    else:
        form = UserRegisterForm()


    data = {
        'form':form,
    }
    return render(request,'accounts/signup.html',data)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            messages.success(request,f'Logged in as {user.get_username()}!')
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:    
                return redirect('articles:list')
    else:
        form = AuthenticationForm()

        data = {
        'form':form,
    }

    return render(request,'accounts/login.html',data)


def logout_view(request):
    logout(request)
    messages.info(request,f'You have been logged out!')
    return redirect('accounts:login')

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST,instance=request.user)
        profile_picture_form = ProfileUpdateForm(request.POST,request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_picture_form.is_valid():
            user_form.save()
            profile_picture_form.save()
            messages.success(request,f'Profile Updated')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_picture_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form':user_form,
        'profile_picture_form':profile_picture_form,
    }
    return render(request,'accounts/profile.html',context)