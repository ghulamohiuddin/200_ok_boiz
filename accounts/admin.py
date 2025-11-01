from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import User, SeekerProfile, Interest
from .models import FinderProfile, OpportunityType

@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    fieldsets = DefaultUserAdmin.fieldsets + (
        ('Extra', {
            'fields': (
                'is_talent_finder',
                'is_talent_seeker',
                'bio',
                'skills',
                'profile_picture',
                'resume',
            ),
        }),
    )
    list_display = ('username', 'email', 'is_talent_finder', 'is_talent_seeker', 'is_staff')


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(SeekerProfile)
class SeekerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'university', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'university', 'skills')
    filter_horizontal = ('interests',)



@admin.register(OpportunityType)
class OpportunityTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(FinderProfile)
class FinderProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'created_at')
    search_fields = ('user__username', 'organization')
    filter_horizontal = ('opportunities',)

