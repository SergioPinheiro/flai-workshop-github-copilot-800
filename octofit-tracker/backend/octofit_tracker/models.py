from django.db import models
from django.core.validators import EmailValidator
from djongo import models as djongo_models


class Team(djongo_models.Model):
    TEAM_CHOICES = [
        ('marvel', 'Team Marvel'),
        ('dc', 'Team DC'),
    ]

    _id = djongo_models.ObjectIdField()
    name = models.CharField(max_length=255, choices=TEAM_CHOICES)
    description = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = djongo_models.DjongoManager()

    class Meta:
        db_table = 'teams'

    def __str__(self):
        return self.name



class User(djongo_models.Model):
    _id = djongo_models.ObjectIdField()
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    name = models.CharField(max_length=255)
    superhero_name = models.CharField(max_length=255, default='')
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = djongo_models.DjongoManager()

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.name} ({self.superhero_name})"


class Activity(djongo_models.Model):
    ACTIVITY_TYPES = [
        ('running', 'Running'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('walking', 'Walking'),
        ('strength_training', 'Strength Training'),
    ]

    _id = djongo_models.ObjectIdField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)
    description = models.TextField(default='')
    duration_minutes = models.IntegerField()
    calories_burned = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = djongo_models.DjongoManager()

    class Meta:
        db_table = 'activities'

    def __str__(self):
        return f"{self.user.name} - {self.activity_type}"


class Leaderboard(djongo_models.Model):
    _id = djongo_models.ObjectIdField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_points = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    total_activities = models.IntegerField(default=0)
    total_calories_burned = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    objects = djongo_models.DjongoManager()

    class Meta:
        db_table = 'leaderboard'
        ordering = ['-total_points']

    def __str__(self):
        return f"{self.user.name} - Rank {self.rank}"


class Workout(djongo_models.Model):
    WORKOUT_TYPES = [
        ('cardio', 'Cardio'),
        ('strength', 'Strength'),
        ('flexibility', 'Flexibility'),
        ('balance', 'Balance'),
    ]

    _id = djongo_models.ObjectIdField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    workout_type = models.CharField(max_length=50, choices=WORKOUT_TYPES)
    duration_minutes = models.IntegerField()
    difficulty_level = models.CharField(max_length=20, choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')])
    instructions = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = djongo_models.DjongoManager()

    class Meta:
        db_table = 'workouts'

    def __str__(self):
        return self.name

