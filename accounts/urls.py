# accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Auth
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Profile
    path('profile/', views.profile_view, name='profile'),

    # Role selection
    path('role-selection/', views.RoleSelectionView.as_view(), name='role_selection'),
    path('set-role/<str:role>/', views.SetRoleView.as_view(), name='set_role'),

    # Setup pages
    path('seeker-setup/', views.SeekerSetupView.as_view(), name='seeker_setup'),
    path('finder-setup/', views.FinderProfileSetupView.as_view(), name='finder_setup'),

    # Dashboards
    path('seeker-dashboard/', views.SeekerDashboardView.as_view(), name='seeker_dashboard'),
    path('finder-dashboard/', views.FinderDashboardView.as_view(), name='finder_dashboard'),
]
