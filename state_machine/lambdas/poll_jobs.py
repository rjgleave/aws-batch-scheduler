import json
import boto3

print('Loading poll_jobs function...')
batch = boto3.client('batch')

def poll_job(job):
    data = job.get("jobId", "")
    jobId = data['jobId']

    try:
        # Call DescribeJobs
        response = batch.describe_jobs(jobs=[jobId])
        # Log response from AWS Batch
        print("Response: " + json.dumps(response, indent=2))
        # Return the jobtatus
        if response['jobs']:
            job['jobStatus'] = response['jobs'][0]['status']
        else:
            job['jobStatus'] = "NOTFOUND"
        return job
    except Exception as e:
        print(e)
        message = 'Error getting Batch Job status'
        print(message)
        raise Exception(message)


def lambda_handler(event, context):
    # Log the received event
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the joblist from the event
    jobList = event['jobList']
    scheduleFail = False
    scheduleRunning = False

    # iterate through the jobs to get the current status of each
    i=0
    for j in jobList:
        event['jobList'][i] = poll_job(j)
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
        i = i + 1

    # return updated document
    if scheduleFail:
        event['scheduleStatus'] = "FAILED"
    else:
        if scheduleRunning:
            event['scheduleStatus'] = "RUNNING"
        else:
            event['scheduleStatus'] = "SUCCEEDED"

    return event
