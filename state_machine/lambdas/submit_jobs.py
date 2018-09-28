import json
import boto3

batch = boto3.client('batch')
print('Loading submit_jobs function...')

def submit_batch_job(job, jobList):
    # lookup job id for the given job name
    '''
    def get_jobid_for_jobname(jobName, jobList):
        for j in jobList:
            if j['jobName'] == jobName:
                return j['jobId']
    '''  
    # lookup job id for the given job name
    # NOTE:  this is a band-aid - works but the one above should be, but isn't
    def get_jobid_for_jobname(jobName, jobList):
        jid = ""
        for j in jobList:
            if j['jobName'] == jobName:
                jid = j['jobId']
        if type(jid) == dict:
            jid = jid['jobId']
        return jid

    jobName = job['jobName']
    jobQueue = job['jobQueue']
    jobDefinition = job['jobDefinition']
    # containerOverrides and parameters are optional
    if job.get('containerOverrides'):
        containerOverrides = job['containerOverrides']
    else:
        containerOverrides = {}
    if job.get('parameters'):
        parameters = job['parameters']
    else:
        parameters = {}
    
    # generate the Batch job dependency parameter
    nameList = job['jobDependencies']
    depOn=[]
    for name in nameList:
        for j in jobList:
            # NOTE: special logic below to skip (PASS) failed job steps.   If you manually
            # change the job status to PASS in the schedule history record, it will skip 
            # that failed step
            if j['jobName'] == name and j['jobStatus'] != 'PASS':
                # get the job ID of the batch instance
                jid = j.get('jobId')
                if type(jid) == dict:
                    jid = jid['jobId']
                # now create parameter
                ddict={}
                ddict['type']='SEQUENTIAL'
                ddict['jobId']=jid
                # create the dependency statement
                depOn.append(ddict)
                break

    #dep = get_dependencies(job['jobDependencies'], jobList)

    try:
        # Submit a Batch Job
        response = batch.submit_job(jobQueue=jobQueue, jobName=jobName, jobDefinition=jobDefinition,
                                    containerOverrides=containerOverrides, parameters=parameters,
                                     dependsOn = depOn)
        # Log response from AWS Batch
        print("Response: " + json.dumps(response, indent=2))
        # Return the jobId
        jobId = response['jobId']
        return {
            'jobId': jobId
        }
    except Exception as e:
        event['scheduleMessage'] = e.response['Error']['Message']
        print(event['scheduleMessage'])
        raise Exception(message)
        event['jobStatus'] = "FAILED" 


def lambda_handler(event, context):
    # Log the received event
    print("Received event: " + json.dumps(event, indent=2))

    # Get the joblist from the event
    jobList = event['jobList']

    # iterate through the jobs to get the current status of each
    i=0
    for j in jobList:
        # NOTE: special logic below to skip (PASS) failed job steps.   If you manually
        # change the job status to PASS in the schedule history record, it will skip 
        # that failed step
        if j['jobStatus'] == "SUCCEEDED" or j['jobStatus'] == "PASS":
            pass
        else:
            if j['jobStatus'] == "FAILED" or j['jobStatus'] == "NOTFOUND":
                scheduleFail = True
            else:
                scheduleRunning = True
                # submit the batch
                jobId = submit_batch_job(j, jobList)
                print("submitted! jobId is: ", jobId)
                if jobId:
                    #print "job status: ", jobStatus
                    # update the step functions document with the job id
                    event['jobList'][i]['jobId'] = jobId 
                    # update schedule status to Running
                    event['scheduleStatus'] = "RUNNING"
        i = i + 1

    return event