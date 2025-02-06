from .models import Profile
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm,InfiniteFlightDetailsForm, MembershipTestForm, FlightReplayForm

# View for user registration
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Log the user in after registration
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')  # Redirect to the dashboard
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})



# View for user login
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # Log the user in
                messages.success(request, f'Welcome back, {username}!')
                return redirect('dashboard')  # Redirect to the dashboard
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

# View for user logout
def user_logout(request):
    logout(request)  # Log the user out
    messages.success(request, 'You have been logged out.')
    return redirect('home')  # Redirect to the home page

# View for the dashboard (protected route)
@login_required  # Ensures only logged-in users can access this view
def dashboard(request):

    user_profile = request.user.profile

    return render(request, 'users/dashboard.html', {'user': request.user, 'user_profile': user_profile})

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    profiles = Profile.objects.filter(rank='Cadet Under Review')
    return render(request, 'admin/dashboard.html', {'profiles': profiles})

# View for Membership Application
@login_required
def membership_application(request):
    user_profile = request.user.profile

    # Step 1: Infinite Flight Username Submission (Membership Pending)
    if user_profile.rank == 'Membership Pending':
        if user_profile.infinite_flight_username:  # Check if already submitted
            return redirect('dashboard')  # Prevent multiple submissions

        if request.method == 'POST':
            form = InfiniteFlightDetailsForm(request.POST)
            if form.is_valid():
                user_profile.infinite_flight_username = form.cleaned_data['infinite_flight_username']
                user_profile.rank = 'Cadet Applicant'  # Admin will change rank later
                user_profile.save()
                messages.success(request, "Your Infinite Flight username has been submitted successfully!")
                return redirect('dashboard')  # Redirect to dashboard after submission
        else:
            form = InfiniteFlightDetailsForm()

        return render(request, 'users/membership_application.html', {'user': request.user, 'form': form, 'step': 1})

    # Step 2: Membership Test (Cadet)
    elif user_profile.rank == 'Cadet':
        if request.method == 'POST':
            form = MembershipTestForm(request.POST)
            if form.is_valid():
                user_profile.rank = 'Second Officer'  # Admin should review and approve
                user_profile.save()
                return redirect('membership_application')
        else:
            form = MembershipTestForm()

        return render(request, 'users/membership_application.html', {'user': request.user, 'form': form, 'step': 2})

    # Step 3: Practical Test (Second Officer)
    elif user_profile.rank == 'Second Officer':
        if request.method == 'POST':
            form = FlightReplayForm(request.POST, request.FILES)
            if form.is_valid():
                user_profile.rank = 'First Officer Applicant'  # Admin should confirm manually
                user_profile.save()
                messages.success(request, "Your flight replay has been submitted successfully!")

                return redirect('membership_application')
        else:
            form = FlightReplayForm()

        return render(request, 'users/membership_application.html', {'user': request.user, 'form': form, 'step': 3})

    # Redirect to dashboard if user has completed the process
    return redirect('dashboard')


# View for Account deletion
@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)  # Log the user out
        user.delete()  # Delete the user account
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('home')  # Redirect to the home page after deletion
    return redirect('dashboard')  # Redirect back to the dashboard if not a POST request

# View for Profile Pic
def profile(request):
    # Handle profile picture update
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the same page after updating
    else:
        form = ProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'form': form})