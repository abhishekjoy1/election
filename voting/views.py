from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from rest_framework import generics
import pdb

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        pdb.set_trace()
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
    pdb.set_trace()
    return render_to_response(
    'home.html',
    { 'user': request.user }
    )

@login_required
def vote(request):
    return render_to_response(
    'cast_vote.html',
    { 'user': request.user,
      'parties': Party.objects.all()
    },
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