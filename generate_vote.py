#!/usr/bin/env python
import os
from random import randint
from voting.models import *
seats=Seat.objects.all()
for seat in seats:
            booths = seat.booth_set.all()
            for booth in booths:
                    file_name='voting_data/District'+str(seat.id)+'/booth-'+str(booth.id)+'.txt'
                    if not os.path.exists('voting_data/District'+str(seat.id)):
                        os.mkdir('voting_data/District'+str(seat.id))
                    i=1
                    while i<=10:
                           parties=Party.objects.all().values('name')
                           index=randint(0,len(parties)-1)
                           party_name=parties[index]['name']
                           f = open(file_name, 'a+' )
                           f.write(party_name+"\n")
                           f.close()
                           i+=1
