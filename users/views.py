from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import CustomUser
from reports.models import IncidentReport
from gamification.models import UserBadge, Activity

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Account created successfully!')
                return redirect('home')
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
                print(f"Registration error: {e}")  # Debug print
        else:
            # Print form errors for debugging
            print("Form errors:", form.errors)
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        # Handle profile update
        user = request.user
        user.phone_number = request.POST.get('phone_number', '')
        user.organization = request.POST.get('organization', '')
        user.bio = request.POST.get('bio', '')
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'registration/profile.html')

@login_required
def dashboard(request):
    user_reports = IncidentReport.objects.filter(reporter=request.user).order_by('-created_at')[:5]
    user_activities = Activity.objects.filter(user=request.user).order_by('-created_at')[:10]
    
    context = {
        'user_reports': user_reports,
        'user_activities': user_activities,
    }
    
    if request.user.user_type in ['ngo', 'government', 'researcher']:
        # Show reports that need validation
        pending_reports = IncidentReport.objects.filter(status='reported').order_by('-created_at')[:5]
        context['pending_reports'] = pending_reports
        
    return render(request, 'users/dashboard.html', context)

def leaderboard(request):
    top_users = CustomUser.objects.order_by('-points')[:20]
    return render(request, 'users/leaderboard.html', {'top_users': top_users})