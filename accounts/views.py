# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm, LoginForm, SeekerProfileForm, FinderProfileForm
from .models import User, SeekerProfile, Interest
from .models import FinderProfile
from .forms import FinderProfileForm



# ==============================
# AUTH VIEWS
# ==============================

class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'accounts/signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST, request.FILES or None)
        if form.is_valid():
            user = form.save(commit=False)
            # default role (can switch later)
            if not user.is_talent_finder and not user.is_talent_seeker:
                user.is_talent_seeker = True
            user.save()
            login(request, user)
            # Redirect to role-selection page after signup
            return redirect('accounts:role_selection')
        return render(request, 'accounts/signup.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # ✅ Redirect to role selection instead of profile
            return redirect('accounts:role_selection')
        return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')  # Replace with your homepage route name


# ==============================
# PROFILE VIEW (basic info edit)
# ==============================

@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        user.bio = request.POST.get('bio', user.bio)
        user.skills = request.POST.get('skills', user.skills)
        user.is_talent_finder = bool(request.POST.get('is_talent_finder'))
        user.is_talent_seeker = bool(request.POST.get('is_talent_seeker'))

        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        if 'resume' in request.FILES:
            user.resume = request.FILES['resume']

        user.save()
        return redirect('accounts:profile')

    return render(request, 'accounts/profile.html', {'user': user})


# ==============================
# ROLE SELECTION
# ==============================

@method_decorator(login_required, name='dispatch')
class RoleSelectionView(View):
    def get(self, request):
        return render(request, 'accounts/role_selection.html')


@method_decorator(login_required, name='dispatch')
class SetRoleView(View):
    def post(self, request, role):
        user = request.user

        if role == 'seeker':
            user.is_talent_seeker = True
            user.is_talent_finder = False
            user.save()
            # redirect to seeker setup form
            return redirect('accounts:seeker_setup')

        elif role == 'finder':
            user.is_talent_finder = True
            user.is_talent_seeker = False
            user.save()
            # redirect to finder setup form
            return redirect('accounts:finder_setup')

        # fallback
        return redirect('accounts:role_selection')


# ==============================
# SEEKER SETUP
# ==============================

@method_decorator(login_required, name='dispatch')
class SeekerSetupView(View):
    template_name = 'accounts/seeker_setup.html'

    def get(self, request):
        profile, created = SeekerProfile.objects.get_or_create(user=request.user)
        form = SeekerProfileForm(instance=profile)

        # create default interests if missing
        if Interest.objects.count() == 0:
            defaults = [
                ('part-time', 'Part-time Jobs'),
                ('internships', 'Internships'),
                ('projects', 'Academic Projects'),
                ('startups', 'Startups'),
                ('competitions', 'Competitions'),
            ]
            for slug, name in defaults:
                Interest.objects.get_or_create(slug=slug, defaults={'name': name})

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        profile, created = SeekerProfile.objects.get_or_create(user=request.user)
        form = SeekerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            form.save_m2m()

            # update user role
            request.user.is_talent_seeker = True
            request.user.is_talent_finder = False
            request.user.save()

            # redirect to seeker dashboard
            return redirect('accounts:seeker_dashboard')

        return render(request, self.template_name, {'form': form})


# ==============================
# FINDER SETUP
# ==============================

@method_decorator(login_required, name='dispatch')
class FinderProfileSetupView(View):
    template_name = 'accounts/finder_setup.html'

    def get(self, request):
        form = FinderProfileForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = FinderProfileForm(request.POST)
        if form.is_valid():
            finder_profile = form.save(commit=False)
            finder_profile.user = request.user
            finder_profile.save()
            form.save_m2m()
            return redirect('accounts:finder_dashboard')

        return render(request, self.template_name, {'form': form})


# ==============================
# DASHBOARD VIEWS
# ==============================

class SeekerDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'accounts/seeker_dashboard.html')


class FinderDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'accounts/finder_dashboard.html')




class FinderProfileSetupView(LoginRequiredMixin, View):
    template_name = 'accounts/finder_setup.html'

    def get(self, request):
        form = FinderProfileForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = FinderProfileForm(request.POST)
        if form.is_valid():
            finder_profile = form.save(commit=False)
            finder_profile.user = request.user
            finder_profile.save()
            form.save_m2m()

            # set role flag
            request.user.is_talent_finder = True
            request.user.is_talent_seeker = False
            request.user.save()

            # redirect to finder dashboard
            return redirect('accounts:finder_dashboard')
        return render(request, self.template_name, {'form': form})


class FinderDashboardView(LoginRequiredMixin, View):
    template_name = 'accounts/finder_dashboard.html'

    def get(self, request):
        profile = getattr(request.user, 'finder_profile', None)
        return render(request, self.template_name, {'profile': profile})
