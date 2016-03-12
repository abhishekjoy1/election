from celery import task
import os, pdb
from .models import *
@task()
def seat_count(seat_id):
    # r = redis.StrictRedis(host='localhost', port=6379)
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
            cmd = "hadoop fs -ls /user/joy/"+hadoop_output_dir
            flag = os.system(cmd)
            while(flag):
                flag = os.system(cmd)
            cmd = "bin/hadoop fs -get /user/joy/"+hadoop_output_dir
            os.system(cmd)
            
            seat = Seat.objects.get(pk=seat_id)
            seat.vote_counted = True
            seat.save()
            # r.put("COUNTING_DONE_SEAT_"+seat_id, "True")
            return True
    return False
