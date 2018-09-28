# reset program to prepare a schedule for restart
import json
import boto3

print('Loading reset_job function...')
batch = boto3.client('batch')

# cancel unfinished batch jobs to enable restart
def reset_job(job):
    data = job.get("jobId", "")
    jobId = data['jobId']

    # INSERT RESET LOGIC HERE!
    # Remove batch job ID
    job['jobId'] = " "
    # Reset the job status
    job['jobStatus'] = " "
    return job


def lambda_handler(event, context):
    # Log the received event
    #print("Received event: " + json.dumps(event, indent=2))

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
            # execute reset logic
            event['jobList'][i] = reset_job(j)

        i = i + 1

    # reset the schedule status
    event['scheduleStatus'] = " "

    # Log the returned event
    print("Returned event: " + json.dumps(event, indent=2))

    return event
