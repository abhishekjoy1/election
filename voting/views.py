from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from rest_framework import generics
from django.conf import settings
from .models import *
import os, pdb
import redis

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print "In register request = "+ str(request.POST)
            form.save()
            return HttpResponseRedirect('/voting/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })
    return render_to_response(
    'registration/register.html',
    variables,
    )

def register_success(request):
    print "In success request = "+ str(request)
    return render_to_response(
    'registration/success.html',
    )

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/voting/')

@login_required
def home(request):
    r = redis.StrictRedis(host='localhost', port=6379)
    IS_ELECTION_DONE = r.get("IS_ELECTION_DONE")
    return render_to_response(
    'home.html',
    { 'user': request.user,
      'is_election_done' : IS_ELECTION_DONE=="true"
    },
    context_instance=RequestContext(request)
    )

@login_required
def vote(request):
    r = redis.StrictRedis(host='localhost', port=6379)
    IS_ELECTION_DONE = r.get("IS_ELECTION_DONE")
    if request.method == 'POST':
        user = CustomUser.objects.get(voter_id=request.POST['user'])
        user.casted_vote = True
        user.save()

        party = Party.objects.get(id=request.POST['party_name'])
        party_name = party.name
        num_seats_own = party.num_seats_won
        num_seats_own += 1
        party.save()

        booth = user.booth
        seat_name = booth.seat.name

        dir = 'voting_data/'+seat_name
        if not os.path.exists(dir):
            os.mkdir(dir)

        file_name = dir+"/booth"+'-'+str(booth.id)+".txt"
        f = open(file_name, 'a+' )
        f.write(party_name+"\n")
        f.close()

        return render_to_response(
        'home.html',
        { 'user': request.user,
          'is_election_done' : IS_ELECTION_DONE=="true"
        },
        context_instance=RequestContext(request)
        )
    user = request.user
    if user.casted_vote:
        return render_to_response(
            'home.html',
            { 'user': request.user,
              'is_election_done' : IS_ELECTION_DONE=="true"
            },
            context_instance=RequestContext(request)
        )
    return render_to_response(
        'cast_vote.html',
        { 'user': request.user,
          'parties': Party.objects.all()
        },
        context_instance=RequestContext(request)
    )

@login_required
def update_election_status(request):
    if request.method == 'POST':
        r = redis.StrictRedis(host='localhost', port=6379)
        IS_ELECTION_DONE = r.get("IS_ELECTION_DONE")
        if not IS_ELECTION_DONE:
            r.set("IS_ELECTION_DONE", "true")
        else:
            if IS_ELECTION_DONE == "true":
                IS_ELECTION_DONE = "false"
            else:
                IS_ELECTION_DONE = "true"
            r.set("IS_ELECTION_DONE", IS_ELECTION_DONE)
        return HttpResponse("<a href='/voting/count_vote/'>Count Votes</a>")


@login_required
def count_vote(request):
    if request.method == 'POST':
        seat_id = request.POST['seat_id']
        from voting.tasks import seat_count
        seat_count.delay(seat_id)
        return HttpResponseRedirect('/voting/result_count/')
    states = State.objects.filter(vote_counted=False)
    if len(states) > 0:
        return render_to_response(
            "count_votes.html",
            { 'user': request.user,
              'states': states
            },
            context_instance=RequestContext(request)
        )
    return HttpResponse('/voting/result_count/')

@login_required
def result_count(request):
    # r = redis.StrictRedis(host='localhost', port=6379)
    seats = Seat.objects.filter(vote_counted=True)
    if len(seats) > 0:
        seat_names = seats.values("name")
        return HttpResponse("Counting is over for "+str(seat_names))
    return render_to_response(
        "result_seat.html",
        context_instance=RequestContext(request)
    )


from rest_framework import viewsets
from voting.serializers import CustomUserSerializer, StateSerializer, SeatSerializer, BoothSerializer
from .models import *

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('voter_id')
    serializer_class = CustomUserSerializer

class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all().order_by('name')
    serializer_class = StateSerializer

class SeatViewSet(viewsets.ModelViewSet):
    serializer_class = SeatSerializer

    def get_queryset(self):
        if 'state_id' in self.request.GET:
            state = self.request.GET['state_id']
            return Seat.objects.filter(state=state)
        return Seat.objects.all()

class BoothViewSet(viewsets.ModelViewSet):
    serializer_class = BoothSerializer

    def get_queryset(self):
        if 'seat_id' in self.request.GET:
            seat = self.request.GET['seat_id']
            return Booth.objects.filter(seat=seat)
        return Booth.objects.all()