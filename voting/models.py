from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)

class StateManager(models.Manager):
    def get_by_natural_key(self, id):
        return self.get(pk=id)

class State(models.Model):
    name = models.CharField(max_length=200)
    objects = StateManager()

    def __str__(self):
        return "%s" % (self.name)

class Seat(models.Model):
    name = models.CharField(max_length=200)
    state = models.ForeignKey(State)

    def __str__(self):
        return "%s" % (self.name)

class Booth(models.Model):
    name = models.CharField(max_length=200)
    seat = models.ForeignKey(Seat)

    def __str__(self):
        return "%s" % (self.name)

class Party(models.Model):
    name = models.CharField(max_length=200)
    num_seats_won = models.IntegerField(default=0)

    def __str__(self):
        return "%s" % (self.name)

SEX = (('M', 'MALE'), ('F', 'FEMALE'))

class CustomUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, date_of_birth, sex, is_election_staff, voter_id, password=None):
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            sex=sex,
            is_election_staff=is_election_staff,
            voter_id=voter_id
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,
            date_of_birth=date_of_birth
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    sex = models.CharField(choices=SEX, max_length=10)
    is_election_staff = models.BooleanField(default=True)
    voter_id = models.CharField(max_length=40, unique=True)
    booth = models.ForeignKey(Booth)
    casted_vote = models.BooleanField(default=False)

    USERNAME_FIELD = 'voter_id'

    objects = CustomUserManager()

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


