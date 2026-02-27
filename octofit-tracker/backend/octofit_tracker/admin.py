from django.contrib import admin
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Admin configuration for Team model."""
    list_display = ('name', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin configuration for User model."""
    list_display = ('name', 'email', 'superhero_name', 'team', 'created_at')
    list_filter = ('team', 'created_at', 'updated_at')
    search_fields = ('name', 'email', 'superhero_name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User Information', {
            'fields': ('name', 'email', 'superhero_name')
        }),
        ('Team Assignment', {
            'fields': ('team',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin configuration for Activity model."""
    list_display = ('user', 'activity_type', 'duration_minutes', 'calories_burned', 'timestamp')
    list_filter = ('activity_type', 'timestamp', 'user__team')
    search_fields = ('user__name', 'user__superhero_name', 'description')
    readonly_fields = ('timestamp',)
    fieldsets = (
        ('Activity Information', {
            'fields': ('user', 'activity_type', 'description')
        }),
        ('Performance Metrics', {
            'fields': ('duration_minutes', 'calories_burned')
        }),
        ('Timestamps', {
            'fields': ('timestamp',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    """Admin configuration for Leaderboard model."""
    list_display = ('user', 'rank', 'total_points', 'total_activities', 'total_calories_burned')
    list_filter = ('rank', 'updated_at', 'user__team')
    search_fields = ('user__name', 'user__superhero_name')
    readonly_fields = ('updated_at',)
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Leaderboard Metrics', {
            'fields': ('rank', 'total_points', 'total_activities', 'total_calories_burned')
        }),
        ('Timestamps', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    """Admin configuration for Workout model."""
    list_display = ('name', 'workout_type', 'difficulty_level', 'duration_minutes', 'created_at')
    list_filter = ('workout_type', 'difficulty_level', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Workout Information', {
            'fields': ('name', 'description', 'instructions')
        }),
        ('Workout Details', {
            'fields': ('workout_type', 'difficulty_level', 'duration_minutes')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
