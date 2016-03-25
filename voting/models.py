from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)

class StateManager(models.Manager):
    def get_by_natural_key(self, id):
        return self.get(pk=id)

class State(models.Model):
    name = models.CharField(max_length=200, unique=True)
    vote_counted = models.BooleanField(default=False)
    objects = StateManager()

    def __str__(self):
        return "%s" % (self.name)

class Seat(models.Model):
    name = models.CharField(max_length=200)
    state = models.ForeignKey(State)
    vote_counted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('state', 'name',)

    def __str__(self):
        return "%s" % (self.name)

class Booth(models.Model):
    name = models.CharField(max_length=200)
    seat = models.ForeignKey(Seat)

    class Meta:
        unique_together = ('seat', 'name',)

    def __str__(self):
        return "%s" % (self.name)

class Party(models.Model):
    name = models.CharField(max_length=200, unique=True)
    num_seats_won = models.IntegerField(default=0)

    def __str__(self):
        return "%s" % (self.name)

SEX = (('M', 'MALE'), ('F', 'FEMALE'))

class CustomUserManager(BaseUserManager):
    def create_user(self, first_name, voter_id, is_election_staff=False, last_name=None, sex=None, date_of_birth=None, password=None):
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

    def create_superuser(self, voter_id, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            first_name='admin',
            last_name='',
            is_election_staff=True,
            password=password,
            voter_id=voter_id
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True)
    sex = models.CharField(choices=SEX, max_length=10, null=True)
    is_election_staff = models.BooleanField(default=True)
    voter_id = models.CharField(max_length=40, unique=True)
    booth = models.ForeignKey(Booth, null=True)
    casted_vote = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'voter_id'

    objects = CustomUserManager()

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    def get_full_name(self):
        return self.first_name+" "+self.last_name

    def get_short_name(self):
        return self.first_name



