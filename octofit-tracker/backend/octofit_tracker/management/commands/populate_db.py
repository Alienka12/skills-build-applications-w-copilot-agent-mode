
from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from datetime import date
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Drop collections using PyMongo for a clean slate
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        db['users'].drop()
        db['teams'].drop()
        db['activities'].drop()
        db['workouts'].drop()
        db['leaderboard'].drop()

        # Create Teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create Users
        tony = User.objects.create(name='Tony Stark', email='tony@marvel.com', team=marvel)
        steve = User.objects.create(name='Steve Rogers', email='steve@marvel.com', team=marvel)
        bruce = User.objects.create(name='Bruce Wayne', email='bruce@dc.com', team=dc)
        clark = User.objects.create(name='Clark Kent', email='clark@dc.com', team=dc)

        # Create Workouts
        w1 = Workout.objects.create(name='Super Strength', description='Heavy lifting and power moves', difficulty='Hard')
        w2 = Workout.objects.create(name='Flight Training', description='Aerial maneuvers and endurance', difficulty='Medium')

        # Create Activities
        Activity.objects.create(user=tony, type='Iron Suit Training', duration=60, date=date.today())
        Activity.objects.create(user=steve, type='Shield Practice', duration=45, date=date.today())
        Activity.objects.create(user=bruce, type='Martial Arts', duration=50, date=date.today())
        Activity.objects.create(user=clark, type='Flying', duration=70, date=date.today())

        # Create Leaderboard
        Leaderboard.objects.create(user=tony, score=100)
        Leaderboard.objects.create(user=steve, score=90)
        Leaderboard.objects.create(user=bruce, score=95)
        Leaderboard.objects.create(user=clark, score=98)

        # Ensure unique index on email for users
        db['users'].create_index([('email', 1)], unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
