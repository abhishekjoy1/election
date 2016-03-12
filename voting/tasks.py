from celery import task
import os, pdb
from .models import *
@task()
def seat_count(seat_id):
    hadoop_input_dir = 'voting_data/Seat'+seat_id+'/'
    if not os.path.exists(hadoop_input_dir):
        return False
    hadoop_output_dir = 'Result_Seat'+seat_id
    cmd = "hadoop fs -put "+ hadoop_input_dir + " /user/joy/"
    flag = os.system(cmd)
    if not flag:
        cmd = "hadoop jar VoteCount.jar "+ "/user/joy/Seat"+seat_id + " " + "/user/joy/"+hadoop_output_dir
        flag = os.system(cmd)
        if not flag:
            seat = Seat.objects.get(pk=seat_id)
            seat.vote_counted = True
            seat.save()
            return True
    return False
