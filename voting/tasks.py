from celery import task
import os, pdb
from models import *
import operator
@task()
def seat_count(seat_id, state_id):#the task to run for a district under a state
    file_name = 'voting_data/State'+str(state_id)+"/district"+'-'+str(seat_id)+".txt" #if output already exists then hadoop will not run
    if os.path.exists(file_name):
        return True
    hadoop_input_dir = 'voting_data/District'+str(seat_id) #hadoop input for each district that contains the casted votes booth wise
    if not os.path.exists(hadoop_input_dir):#if input directory does not exist then there is nothing to run on hadoop
        return False
    hadoop_output_dir = 'Result_District'+str(seat_id) #output folder that is generated for each district
    cmd = "hadoop fs -put "+hadoop_input_dir+ " /user/joy/" #command to copy the input of hadoop from local file system to hdfs
    flag = os.system(cmd) #flag contains the status of the command-nonzero means failure otherwise successs
    if not flag: #if success
        cmd = "hadoop jar VoteCount.jar "+ "/user/joy/District"+ str(seat_id) + " " + "/user/joy/"+hadoop_output_dir #command to run the job on hadoop for each district
        flag = os.system(cmd)
        if not flag:
            cmd = "hadoop fs -ls /user/joy/"+hadoop_output_dir+'/part-r-00000' #command to check whether output has been generated by hadoop
            flag = os.system(cmd)
            while(flag): #keep on looping until the output file is generated
                flag = os.system(cmd)
            cmd = "hadoop fs -get /user/joy/"+hadoop_output_dir+"/part-r-00000 "+hadoop_input_dir+'/count' #command to copy the output directory from hdfs to local file system
            os.system(cmd)


            lines = [line.rstrip('\n') for line in open(hadoop_input_dir+"/count")] #read contents of the output file line by line
            parties_with_votes = [l.split("\t") for l in lines]
            winner = max(parties_with_votes, key=operator.itemgetter(1))[0] #parsing and finding party with maximum votes


            if not os.path.exists('voting_data/State'+str(state_id)): #check whether directory exists for corresponding state that is required as input for state level
                os.mkdir('voting_data/State'+str(state_id))  #if not, create the directory


            f = open(file_name, 'a+' )   #open the output file that is required as input at state level in append mode
            f.write(winner+" 1"+"\n")
            f.close()
            return True
    return False

@task()
def state_count(state_id):
    file_name = 'voting_data/state'+str(state_id)+".txt" #if output already exists then hadoop will not run
    if os.path.exists(file_name):
        return True
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