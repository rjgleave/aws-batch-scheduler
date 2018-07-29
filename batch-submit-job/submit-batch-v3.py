#
# Copyright 2013-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the
# License. A copy of the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "LICENSE.txt" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES
# OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions and
# limitations under the License.
#
# Submits an image classification training job to an AWS Batch job queue, and tails the CloudWatch log output.
#

import argparse
import sys
import time
from datetime import datetime
import json
import decimal
import boto3
from botocore.compat import total_seconds
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
# set up dynamoDB table 
table = dynamodb.Table('jobSchedule')

batch = boto3.client(
    service_name='batch',
    region_name='us-east-2',
    endpoint_url='https://batch.us-east-2.amazonaws.com')

cloudwatch = boto3.client(
    service_name='logs',
    region_name='us-east-2',
    endpoint_url='https://logs.us-east-2.amazonaws.com')

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--name", help="name of the job", type=str, default='run a remote command')
parser.add_argument("--job-queue", help="name of the job queue to submit this job", type=str, default='JobQueue-911b8f5446a4d90')
parser.add_argument("--job-definition", help="name of the job job definition", type=str, default='remote_jobd:6')
parser.add_argument("--command", help="command to run", type=str,default='echo hello')
parser.add_argument("--wait", help="block wait until the job completes", action='store_true')

args = parser.parse_args()

## Classes -------------------------------------------------------------------
## Job Schedule Class - for the main schedule
class JsSchedule(object):
    """__init__() functions as the class constructor"""
    def __init__(self, name=None, description=None, status=None, jobarray=None):
        self.Name = name
        self.Description = description
        self.Status = status
        self.JobArray = jobarray

    # if you need to print the class...  here is how >>  print(obj)
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

# Job Schedule class - for each submitted job
class JsJob(object):
    """__init__() functions as the class constructor"""
    def __init__(self, jobname=None, command=None, jobdependencies=None ):
        self.JobName = jobname
        self.Command = command
        self.JobDependencies = jobdependencies

    # if you need to print the class...  here is how >>  print(obj)
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    # return the list of dependent jobs
    def get_dependencies(self, jobArray):
        depOn=[]
        try:
            jList = self.JobDependencies.split(",")
        except:
            try:
                jList = self.JobDependencies.split()
            except:
                print "JobDependencies: ", self.JobDependencies, " could not be loaded"

        # generate a parameter string segment
        for j in range(len(jList)):
            # get jobID from submitted jobs list (job array)
            try:
                ddict={}
                ddict['type']='SEQUENTIAL'
                ddict['jobId']=jobArray[jList[j]]
                # create the dependency statement
                depOn.append(ddict)
            except:
                print "JobID lookup FAILED"

        return depOn
    

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)

## Functions -----------------------------------------------------------------

def dump(obj):
  for attr in dir(obj):
    print("obj.%s = %r" % (attr, getattr(obj, attr)))

## MAIN  ---------------------------------------------------------------------

def main():
    spin = ['-', '/', '|', '\\', '-', '/', '|', '\\']
    logGroupName = '/aws/batch/job'

    jobName = args.name
    jQueue = args.job_queue
    jDefinition = args.job_definition
    command = args.command.split()

    job_schedule = 'EDW_Recycle_CalcConsumer_Box'
    print("Jobs for schedule: " + job_schedule)

    ddb_response = table.query(
        KeyConditionExpression=Key('ScheduleName').eq('EDW_Recycle_CalcConsumer_Box') 
    )

    # create a dictionary for the job array
    jobArray = {}

    # read all job steps for the schedule
    for i in ddb_response['Items']:
        # create class objects
        if i['RecordType'] == 'HEADER':
            jsch = JsSchedule(i['ScheduleName'],i['Description'], "running", {})
            continue   
        elif i['RecordType'] == 'JOB':
            jjob = JsJob(i['JobName'],i['Command'],i['JobDependencies'])         
        else:
            print "Invalid RecordType in Schedule table >>: ", i['RecordType']
            continue
        JobName = i['JobName']

        # Submit job to the queue
        s_resp = batch.submit_job(
            jobName=jjob.JobName,
            jobQueue=jQueue,
            jobDefinition=jDefinition,
            dependsOn = jjob.get_dependencies(jsch.JobArray)
        )

        # add the current job/JobID key/value pairs to the list of submitted jobs
        #jobArray[JobName]= s_resp['jobId']
        jsch.JobArray[jjob.JobName] = s_resp['jobId']

        print("Submitted Job: {}, JobId: {}, Runs After: {}".format(jjob.JobName,s_resp['jobId'],str(jjob.JobDependencies)))    


    print(jsch) 

if __name__ == '__main__':
    try: main()
    except: raise
