from django.test import TestCase
from rest_framework.test import APIClient
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout


class TeamTestCase(TestCase):
    """Test cases for Team model and endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(
            name='marvel',
            description='Team Marvel superhero group'
        )

    def test_team_creation(self):
        """Test creating a team."""
        self.assertEqual(self.team.name, 'marvel')
        self.assertEqual(self.team.description, 'Team Marvel superhero group')

    def test_team_list_endpoint(self):
        """Test listing teams via API."""
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, 200)


class UserTestCase(TestCase):
    """Test cases for User model and endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(
            name='marvel',
            description='Team Marvel'
        )
        self.user = User.objects.create(
            email='tony@stark.com',
            name='Tony Stark',
            superhero_name='Iron Man',
            team=self.team
        )

    def test_user_creation(self):
        """Test creating a user."""
        self.assertEqual(self.user.name, 'Tony Stark')
        self.assertEqual(self.user.superhero_name, 'Iron Man')
        self.assertEqual(self.user.team.name, 'marvel')

    def test_user_list_endpoint(self):
        """Test listing users via API."""
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 200)

    def test_user_activities_endpoint(self):
        """Test retrieving user activities."""
        response = self.client.get(f'/api/users/{self.user.id}/activities/')
        self.assertEqual(response.status_code, 200)


class ActivityTestCase(TestCase):
    """Test cases for Activity model and endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(
            name='marvel',
            description='Team Marvel'
        )
        self.user = User.objects.create(
            email='steve@rogers.com',
            name='Steve Rogers',
            superhero_name='Captain America',
            team=self.team
        )
        self.activity = Activity.objects.create(
            user=self.user,
            activity_type='running',
            description='Morning run',
            duration_minutes=30,
            calories_burned=300
        )

    def test_activity_creation(self):
        """Test creating an activity."""
        self.assertEqual(self.activity.activity_type, 'running')
        self.assertEqual(self.activity.duration_minutes, 30)
        self.assertEqual(self.activity.calories_burned, 300)

    def test_activity_list_endpoint(self):
        """Test listing activities via API."""
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, 200)


class LeaderboardTestCase(TestCase):
    """Test cases for Leaderboard model and endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(
            name='dc',
            description='Team DC'
        )
        self.user = User.objects.create(
            email='bruce@wayne.com',
            name='Bruce Wayne',
            superhero_name='Batman',
            team=self.team
        )
        self.leaderboard = Leaderboard.objects.create(
            user=self.user,
            total_points=1000,
            rank=1,
            total_activities=10,
            total_calories_burned=5000
        )

    def test_leaderboard_creation(self):
        """Test creating a leaderboard entry."""
        self.assertEqual(self.leaderboard.total_points, 1000)
        self.assertEqual(self.leaderboard.rank, 1)

    def test_leaderboard_list_endpoint(self):
        """Test listing leaderboard via API."""
        response = self.client.get('/api/leaderboard/')
        self.assertEqual(response.status_code, 200)

    def test_leaderboard_by_team_endpoint(self):
        """Test filtering leaderboard by team."""
        response = self.client.get('/api/leaderboard/by_team/?team=dc')
        self.assertEqual(response.status_code, 200)


class WorkoutTestCase(TestCase):
    """Test cases for Workout model and endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.workout = Workout.objects.create(
            name='Full Body Strength',
            description='A comprehensive full-body strength training workout',
            workout_type='strength',
            duration_minutes=60,
            difficulty_level='hard',
            instructions='Follow the instructions in the fitness app'
        )

    def test_workout_creation(self):
        """Test creating a workout."""
        self.assertEqual(self.workout.name, 'Full Body Strength')
        self.assertEqual(self.workout.workout_type, 'strength')
        self.assertEqual(self.workout.difficulty_level, 'hard')

    def test_workout_list_endpoint(self):
        """Test listing workouts via API."""
        response = self.client.get('/api/workouts/')
        self.assertEqual(response.status_code, 200)
