from django.core.management.base import BaseCommand
from django.utils import timezone
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import timedelta


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Deleted existing data'))

        # Create teams
        team_marvel = Team.objects.create(
            name='marvel',
            description='The mighty Marvel superheroes team'
        )
        team_dc = Team.objects.create(
            name='dc',
            description='The heroic DC superheroes team'
        )

        self.stdout.write(self.style.SUCCESS('Created teams: Marvel and DC'))

        # Create Marvel users
        marvel_superheroes = [
            {'email': 'peter@marvel.com', 'name': 'Peter Parker', 'superhero_name': 'Spider-Man'},
            {'email': 'tony@marvel.com', 'name': 'Tony Stark', 'superhero_name': 'Iron Man'},
            {'email': 'steve@marvel.com', 'name': 'Steve Rogers', 'superhero_name': 'Captain America'},
            {'email': 'bruce@marvel.com', 'name': 'Bruce Banner', 'superhero_name': 'Hulk'},
            {'email': 'thor@marvel.com', 'name': 'Thor Odinson', 'superhero_name': 'Thor'},
        ]

        # Create DC users
        dc_superheroes = [
            {'email': 'clark@dc.com', 'name': 'Clark Kent', 'superhero_name': 'Superman'},
            {'email': 'bruce.wayne@dc.com', 'name': 'Bruce Wayne', 'superhero_name': 'Batman'},
            {'email': 'diana@dc.com', 'name': 'Diana Prince', 'superhero_name': 'Wonder Woman'},
            {'email': 'barry@dc.com', 'name': 'Barry Allen', 'superhero_name': 'The Flash'},
            {'email': 'arthur@dc.com', 'name': 'Arthur Curry', 'superhero_name': 'Aquaman'},
        ]

        users = []
        
        for hero_data in marvel_superheroes:
            user = User.objects.create(
                email=hero_data['email'],
                name=hero_data['name'],
                superhero_name=hero_data['superhero_name'],
                team=team_marvel
            )
            users.append(user)

        for hero_data in dc_superheroes:
            user = User.objects.create(
                email=hero_data['email'],
                name=hero_data['name'],
                superhero_name=hero_data['superhero_name'],
                team=team_dc
            )
            users.append(user)

        self.stdout.write(self.style.SUCCESS(f'Created {len(users)} superhero users'))

        # Create workouts
        workouts_data = [
            {
                'name': 'Morning Run',
                'description': 'A refreshing morning run to start the day',
                'workout_type': 'cardio',
                'duration_minutes': 30,
                'difficulty_level': 'medium',
                'instructions': 'Run at a steady pace for 30 minutes'
            },
            {
                'name': 'Strength Training',
                'description': 'Full body strength training session',
                'workout_type': 'strength',
                'duration_minutes': 45,
                'difficulty_level': 'hard',
                'instructions': 'Perform 3 sets of 8-10 reps for each exercise'
            },
            {
                'name': 'Yoga Session',
                'description': 'Relaxing yoga for flexibility and balance',
                'workout_type': 'flexibility',
                'duration_minutes': 60,
                'difficulty_level': 'easy',
                'instructions': 'Follow the yoga sequence at your own pace'
            },
            {
                'name': 'HIIT Training',
                'description': 'High intensity interval training',
                'workout_type': 'cardio',
                'duration_minutes': 30,
                'difficulty_level': 'hard',
                'instructions': '30 seconds on, 30 seconds rest, repeat 10 times'
            },
            {
                'name': 'Balance Training',
                'description': 'Improve core balance and stability',
                'workout_type': 'balance',
                'duration_minutes': 20,
                'difficulty_level': 'medium',
                'instructions': 'Practice balance exercises daily'
            },
        ]

        workouts = []
        for workout_data in workouts_data:
            workout = Workout.objects.create(**workout_data)
            workouts.append(workout)

        self.stdout.write(self.style.SUCCESS(f'Created {len(workouts)} workouts'))

        # Create activities for each user
        activity_types = ['running', 'cycling', 'swimming', 'walking', 'strength_training']
        activity_count = 0

        for user in users:
            for i in range(5):
                activity = Activity.objects.create(
                    user=user,
                    activity_type=activity_types[i % len(activity_types)],
                    description=f'{user.superhero_name} completed a {activity_types[i % len(activity_types)]} session',
                    duration_minutes=30 + (i * 5),
                    calories_burned=200 + (i * 50),
                    timestamp=timezone.now() - timedelta(days=i)
                )
                activity_count += 1

        self.stdout.write(self.style.SUCCESS(f'Created {activity_count} activities'))

        # Create leaderboard entries
        for idx, user in enumerate(users, 1):
            total_activities = Activity.objects.filter(user=user).count()
            total_calories = sum(a.calories_burned for a in Activity.objects.filter(user=user))
            
            Leaderboard.objects.create(
                user=user,
                total_points=total_activities * 100,
                rank=idx,
                total_activities=total_activities,
                total_calories_burned=total_calories
            )

        self.stdout.write(self.style.SUCCESS(f'Created {len(users)} leaderboard entries'))
        self.stdout.write(self.style.SUCCESS('Database population completed successfully!'))
