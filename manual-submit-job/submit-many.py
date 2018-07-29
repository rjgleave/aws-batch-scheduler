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

import boto3
from botocore.compat import total_seconds

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
parser.add_argument("--job-definition", help="name of the job job definition", type=str, default='remote_jobd:5')
parser.add_argument("--command", help="command to run", type=str,default='echo hello')
parser.add_argument("--wait", help="block wait until the job completes", action='store_true')

args = parser.parse_args()


def nowInMillis():
    endTime = long(total_seconds(datetime.utcnow() - datetime(1970, 1, 1))) * 1000L
    return endTime

def random_four():
    """Returns a random 4 charactors"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

def main():
    spin = ['-', '/', '|', '\\', '-', '/', '|', '\\']
    logGroupName = '/aws/batch/job'

    jobName = args.name
    jQueue = args.job_queue
    jDefinition = args.job_definition
    command = args.command.split()

    """run(queue,jobdef) Submits 5 jobs, job1, job2[a-c], and job3. The 3 job2 jobs depend on job1, and job3 depends on all job2's."""
    # Creates semi unique job names for each job
    job1Name = 'job1' 
    job2aName = 'job2a' 
    job2bName = 'job2b' 
    job2cName = 'job2c' 
    #job3Name = 'job3' + random_four()
    job3Name = 'job3' 

    # Submit job1 to the qeueu
    job1 = batch.submit_job(
        jobName=job1Name,
        jobQueue=jQueue,
        jobDefinition=jDefinition
    )


    print("Submitted JobName: {}, JobId: {}, Runs After: [ ]".format(job1['jobName'],job1['jobId']))

    # Submit jobs 2a, 2b, 2c, all of which depend on job1
    job2a = batch.submit_job(
        jobName=job2aName,
        jobQueue=jQueue,
        jobDefinition=jDefinition,
        dependsOn=[
            { 
                'jobId': job1['jobId'],
                'type': 'SEQUENTIAL'
            }
        ]
    )

    
    print("Submitted JobName: {}, JobId: {}, Runs After: [ {} ]".format(job2a['jobName'],job2a['jobId'],job1['jobName']))
    job2b = batch.submit_job(
        jobName=job2bName,
        jobQueue=jQueue,
        jobDefinition=jDefinition,
        dependsOn=[
            { 
                'jobId': job1['jobId'],
                'type': 'SEQUENTIAL'
            }
        ]
    )


    print("Submitted JobName: {}, JobId: {}, Runs After: [ {} ]".format(job2b['jobName'],job2b['jobId'],job1['jobName']))
    job2c = batch.submit_job(
        jobName=job2cName,
        jobQueue=jQueue,
        jobDefinition=jDefinition,
        dependsOn=[
            { 
                'jobId': job1['jobId'],
                'type': 'SEQUENTIAL'
            }
        ]
    )


    print("Submitted JobName: {}, JobId: {}, Runs After: [ {} ]".format(job2c['jobName'],job2c['jobId'],job1['jobName']))

    # Submits job3 which depends on job2a, job2b, jobc
    job3 = batch.submit_job(
        jobName=job3Name,
        jobQueue=jQueue,
        jobDefinition=jDefinition,
        dependsOn=[
            { 
                'jobId': job2a['jobId'],
                'type': 'SEQUENTIAL'
            },
            { 
                'jobId': job2b['jobId'],
                'type': 'SEQUENTIAL'
            },
            { 
                'jobId': job2c['jobId'],
                'type': 'SEQUENTIAL'
            }
        ]
    )
    VdependsOn=[
            { 
                'jobId': job2a['jobId'],
                'type': 'SEQUENTIAL'
            },
            { 
                'jobId': job2b['jobId'],
                'type': 'SEQUENTIAL'
            },
            { 
                'jobId': job2c['jobId'],
                'type': 'SEQUENTIAL'
            }
        ]
    

    print("Submitted JobName: {}, JobId: {}, Runs After: [ {}, {}, {} ]".format(job3['jobName'],job3['jobId'],job2a['jobName'],job2b['jobName'],job2c['jobName']))    

if __name__ == "__main__":
    main()
