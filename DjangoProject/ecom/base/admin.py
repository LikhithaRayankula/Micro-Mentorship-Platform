from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import User, Mentor, Availability
from .models import MentorUser


@admin.register(User)
class CustomUserAdmin(DefaultUserAdmin):
    list_display = ('username', 'email', 'is_student', 'is_mentor', 'is_staff')
    list_filter = ('is_student', 'is_mentor', 'is_staff')
    search_fields = ('username', 'email')

class AvailabilityInline(admin.TabularInline):
    model = Availability
    extra = 1

@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ('name', 'qualification', 'job_role', 'is_paid', 'fee')
    search_fields = ('name', 'qualification', 'job_role')
    list_filter = ('is_paid',)
    inlines = [AvailabilityInline]


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('mentor', 'start', 'end')
    list_filter = ('mentor',)


@admin.register(MentorUser)
class MentorUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name')
