from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.conf import settings
from pymongo import MongoClient
from datetime import timedelta
from bson import ObjectId

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]

        # Drop existing collections
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create users
        users = [
            User(_id=ObjectId(), name='thundergod', email='thundergod@mhigh.edu', age=30),
            User(_id=ObjectId(), name='metalgeek', email='metalgeek@mhigh.edu', age=25),
            User(_id=ObjectId(), name='zerocool', email='zerocool@mhigh.edu', age=22),
            User(_id=ObjectId(), name='crashoverride', email='crashoverride@mhigh.edu', age=28),
            User(_id=ObjectId(), name='sleeptoken', email='sleeptoken@mhigh.edu', age=35),
        ]
        User.objects.bulk_create(users)

        # Create teams
        team1 = Team(_id=ObjectId(), name='Blue Team')
        team2 = Team(_id=ObjectId(), name='Gold Team')
        team1.save()
        team2.save()
        for user in users[:3]:
            team1.members.add(user)
        for user in users[3:]:
            team2.members.add(user)

        # Create activities
        activities = [
            Activity(_id=ObjectId(), user=users[0], type='Cycling', duration=3600),
            Activity(_id=ObjectId(), user=users[1], type='Crossfit', duration=7200),
            Activity(_id=ObjectId(), user=users[2], type='Running', duration=5400),
            Activity(_id=ObjectId(), user=users[3], type='Strength', duration=1800),
            Activity(_id=ObjectId(), user=users[4], type='Swimming', duration=4500),
        ]
        Activity.objects.bulk_create(activities)

        # Create leaderboard entries
        leaderboard_entries = [
            Leaderboard(_id=ObjectId(), team=team1, points=100),
            Leaderboard(_id=ObjectId(), team=team2, points=90),
        ]
        Leaderboard.objects.bulk_create(leaderboard_entries)

        # Create workouts
        workouts = [
            Workout(_id=ObjectId(), name='Cycling Training', description='Training for a road cycling event'),
            Workout(_id=ObjectId(), name='Crossfit', description='Training for a crossfit competition'),
            Workout(_id=ObjectId(), name='Running Training', description='Training for a marathon'),
            Workout(_id=ObjectId(), name='Strength Training', description='Training for strength'),
            Workout(_id=ObjectId(), name='Swimming Training', description='Training for a swimming competition'),
        ]
        Workout.objects.bulk_create(workouts)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))