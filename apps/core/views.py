from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from apps.users.models import Profile
from django.http import HttpResponseForbidden
from django.contrib import messages




def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

# View for Member List
def members_list(request):
    # Define your staff roles
    roles = ['CEO', 'Event Manager', 'Marketing Manager', 'HR Manager']  # Add roles as needed

    # Get all users
    users = User.objects.all()

    # Create a list to hold staff members (with default 'Vacant' if no user assigned)
    staff_members = []
    for role in roles:
        profile = Profile.objects.filter(role=role).first()
        if profile:
            staff_members.append({
                'role': role,
                'username': profile.user.username,
            })
        else:
            staff_members.append({
                'role': role,
                'username': 'Vacant',
            })

    # Get the regular pilots from the Profile model
    regular_pilots = [
        {
            'username': user.username,
            'rank': user.profile.rank,  # Access rank from Profile
            'member_since': user.date_joined.strftime('%B %d, %Y'),
            'role': user.profile.role  # Add role from Profile
        }
        for user in users
        if hasattr(user, 'profile') and user.profile.role == 'Pilot'  # Ensure that Profile exists and role is 'Pilot'
    ]

    return render(request, 'core/members_list.html', {'staff_members': staff_members, 'regular_pilots': regular_pilots})
