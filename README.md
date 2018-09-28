Using AWS Batch as a Universal Job Scheduler
============================================

This solution utilizes AWS Batch to execute complex, multi-step job schedules across multiple platforms.   It takes advantage of the powerful AWS Batch job scheduling engine to handle complex job dependencies and automatically execute retries before failing.   It utilizes AWS Step Functions to start the schedule, monitor jobs and record results in AWS DynamoDb.  

![Reference Architecture](https://github.com/rjgleave/aws-batch-universal-scheduler/blob/master/assets/aws-batch-universal-job-scheduler.png)

![](https://github.com/rjgleave/aws-batch-universal-scheduler/blob/master/assets/aws-batch-universal-job-scheduler-legend.png)

This example demonstrates the flexibility of using AWS Batch to act as both a worker actually perform work, or as an orchestrator, to direct other services to perform that work (e.g. AWS Glue, Lambda or EC2).   


What's Here
-----------

This repo includes:

1. README.md - this file and assets folder with images to support it.
2. FOLDER: api-gateway - contains templates to help build and test the API REST interface
    *   test_message_start_machine.json - a sample document to illustrate the message used to trigger the schedule via the API.
3. FOLDER: dynamo - this contains code to help build the sample schedule table in dynamoDB.  It includes:
    *   create_batch_schedule_table.py - this builds the schedule table
    *   write_schedule_record.py - this writes the S3 schedule record into dynamoDb
    *   sample_schedule.json - a sample schedule file which illustrates the structure
    *   create_batch_schedule_history.py - use this to buld the schedule history table.  This table is updated automatically each time a schedule runs.   In addition, failed schedules are restarted using this table.
4. FOLDER: fetch-and-run - contains a generic Docker file and several sample 'fetch' scripts which can be executed from that container.     
5. FOLDER: state_machine  - components to build the state machine
    *   get_job_schedule.py - a lambda to retrieve the job schedule from dynamoDb
    *   poll_jobs.py - a lambda to poll the status of all submitted batch jobs.
    *   submit_jobs.py - lambda function to submit all batch jobs in the schedule. 
    *   JobStatusPollerStateMachine.json - definition of the state machine
    *   input-template.json - an input document that can be used to manually submit the state machine
6. FOLDER: tests - contains several sample templates and scripts for testing the state machine.

Setup Instructions
------------------

Working Backwards, do the following:

1. Create the state machine and batch infrastructure. The easiest way is to use the online jumpstart (sample projects) which will build a basic state machine and all the AWS Batch infrastructure for you. Then you can modify the state machine by replacing the definition with the JobStatusPollerStateMachine definition provided in this repo.
![Step Functions Sample Projects](https://github.com/rjgleave/aws-batch-universal-scheduler/blob/master/assets/step-function-sample-projects.png)

2. Create all the lambdas needed for the state machine (see folder above)
Your state machine should look like this when you are done.

![State Machine](https://github.com/rjgleave/aws-batch-universal-scheduler/blob/master/assets/aws-batch-state-machine2.png)

3. Create a sample schedule (see provided example in the folder above).  Make sure to update it with your batch job queue and other information.

![Sample Schedule](https://github.com/rjgleave/aws-batch-universal-scheduler/blob/master/assets/sample-schedule.png)

4. Create an S3 bucket to hold your job schedules.   Upload the schedule you created in the previous step above.

![S3 Bucket](https://github.com/rjgleave/aws-batch-universal-scheduler/blob/master/assets/s3-bucket.png)

5. Build DynamoDB schedule table and load the S3 schedule into the table (use the programs provided in the folder above)

![DynamoDB](https://github.com/rjgleave/aws-batch-universal-scheduler/blob/master/assets/dynamodb-schedule-table.png)

6. Create a Schedule History table in DynamoDB to hold the processed schedules each time they complete processing.   

7. Test your state machine manually, using the input-template.json document provided in the folder above.

![Input Document](https://github.com/rjgleave/aws-batch-universal-scheduler/blob/master/assets/sample-input-document.png)

8. Create the API which you can use as an alternate mechanism to start the state machine by sending a message.  See the instruction link below if you need help doing that.    Use the provided test message in the folder above.

![API Gateway Message](https://github.com/rjgleave/aws-batch-universal-scheduler/blob/master/assets/sample-api-gateway-message.png)

Other Topics:
-------------
a) Restarting failed jobs:   This can be done by using the RESTART input document or submitting the RESTART message (if using API gateway).   See examples below.

![Restart Messages](https://github.com/rjgleave/aws-batch-universal-scheduler/blob/master/assets/restart-messages2.png)

The key difference between a normal start document and a restart document is the addition of the Start Date/Time as well as the "RESTART" status code. 
Restarts will automatically handle dependencies and know which jobs have complete already to avoid duplicate processing. 

b) Skipping Steps:  Sometimes you may want to skip a certain step during a restart process. If so, you simply find that scheduled instance in the Schedule History table and change the status of that particular job step to "PASS" as illustrated below.  

![Skipping Steps](https://github.com/rjgleave/aws-batch-universal-scheduler/blob/master/assets/skip-step.png)

Then simply restart the job as indicated in section a) above.




__Additional Resources__
AWS documentation: Creating a Step Functions API Using API Gateway
https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-api-gateway.html

AWS Step Functions.
https://aws.amazon.com/step-functions/