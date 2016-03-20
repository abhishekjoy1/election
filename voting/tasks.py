from celery import task
import os, pdb
from models import *
import operator
@task()
def seat_count(seat_id, state_id):
    file_name = 'voting_data/State'+str(state_id)+"/seat"+'-'+str(seat_id)+".txt"
    if os.path.exists(file_name):
        return True
    hadoop_input_dir = 'voting_data/Seat'+str(seat_id)
    if not os.path.exists(hadoop_input_dir):
        return False
    hadoop_output_dir = 'Result_Seat'+str(seat_id)
    cmd = "hadoop fs -put "+hadoop_input_dir+ " /user/joy/"
    flag = os.system(cmd)
    if not flag:
        cmd = "hadoop jar VoteCount.jar "+ "/user/joy/Seat"+ str(seat_id) + " " + "/user/joy/"+hadoop_output_dir
        flag = os.system(cmd)
        if not flag:
            cmd = "hadoop fs -ls /user/joy/"+hadoop_output_dir+'/part-r-00000'
            flag = os.system(cmd)
            while(flag):
                flag = os.system(cmd)
            cmd = "hadoop fs -get /user/joy/"+hadoop_output_dir+"/part-r-00000 "+hadoop_input_dir+'/count'
            os.system(cmd)


            lines = [line.rstrip('\n') for line in open(hadoop_input_dir+"/count")]
            parties_with_votes = [l.split("\t") for l in lines]
            winner = max(parties_with_votes, key=operator.itemgetter(1))[0]


            if not os.path.exists('voting_data/State'+str(state_id)):
                os.mkdir('voting_data/State'+str(state_id))
            f = open(file_name, 'a+' )
            f.write(winner+" 1"+"\n")
            f.close()
            return True
    return False

@task()
def state_count(state_id):
    seat_ids = State.objects.get(pk=state_id).seat_set.all().values('id')
    for seat_id in seat_ids:
        seat_count(seat_id['id'], state_id)
    hadoop_input_dir = 'voting_data/State'+str(state_id)
    if not os.path.exists(hadoop_input_dir):
        return False
    hadoop_output_dir = 'Result_State'+str(state_id)
    cmd = "hadoop fs -put "+ "voting_data/State"+str(state_id)+ " /user/joy/"
    flag = os.system(cmd)
    if not flag:
        cmd = "hadoop jar VoteCount.jar "+ "/user/joy/State"+str(state_id) + " " + "/user/joy/"+hadoop_output_dir
        flag = os.system(cmd)
        if not flag:
            cmd = "hadoop fs -ls /user/joy/"+hadoop_output_dir+'/part-r-00000'
            flag = os.system(cmd)
            while(flag):
                flag = os.system(cmd)
            cmd = "hadoop fs -get /user/joy/"+hadoop_output_dir+"/part-r-00000 "+hadoop_input_dir+'/count'
            os.system(cmd)


            lines = [line.rstrip('\n') for line in open(hadoop_input_dir+"/count")]
            parties_with_votes = [l.split("\t") for l in lines]
            winner = max(parties_with_votes, key=operator.itemgetter(1))[0]


            file_name = 'voting_data/state'+str(state_id)+".txt"
            f = open(file_name, 'a+' )
            f.write(winner+" 1\n")
            f.close()
            return True
    return False