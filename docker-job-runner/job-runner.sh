#!/bin/bash

# you can run this script directly from the command line by:   $ aws ssm li./remote_job.sh <command>
# for example, to issue the 'df' command:    $ aws ssm li./remote_job.sh df
# for example, to issue the 'ps aux' command:    $ aws ssm li./remote_job.sh 'ps aux'


echo "starting up my container"
echo "Args: $@"

# force the region
export AWS_DEFAULT_REGION=us-east-2

###commenting this out for now >>> env
echo "This will test running a remote command on a target machine"
echo ">> jobId: $AWS_BATCH_JOB_ID"

echo "Command executed on target machine: " $1

## run the command on a remote target machine
# sh_command_id=$(aws ssm send-command --document-name "AWS-RunShellScript" --comment "listing RUNNING PROCESSES for a TARGET machine tag" --targets Key=tag:"targetID",Values="Instance-0001" --parameters commands="ps aux" --region us-east-2 --output text --query "Command.CommandId") sh -c 'aws ssm list-command-invocations --command-id "$sh_command_id" --details --query "CommandInvocations[].CommandPlugins[].{Status:Status,Output:Output}"'
aws ssm send-command --document-name "AWS-RunShellScript" --targets Key=tag:"targetID",Values="Instance-0001" --parameters commands="ps" --notification-config "NotificationArn=arn:aws:sns:us-east-2:786247309603:job-completion,NotificationEvents=Success,NotificationType=Command"  --service-role-arn arn:aws:iam::786247309603:role/batchjob-role-rjg --region us-east-2 --output json
#aws ssm send-command --document-name "AWS-RunShellScript" --targets Key=tag:"targetID",Values="Instance-0001" --parameters '{"commands":["#!/usr/bin/python","print \"Hello world from python\""]}' --notification-config "NotificationArn=arn:aws:sns:us-east-2:786247309603:job-completion,NotificationEvents=All,NotificationType=Command"  --service-role-arn arn:aws:iam::786247309603:role/batchjob-role-rjg --region us-east-2 --output json


## simulate a polling delay (for job completion)
date
echo "working... working... working..."
echo "delay time is $delay_time"
sleep 60
date
echo "All Done...bye!!"

## Send email to notify job completion
aws sns publish --topic-arn arn:aws:sns:us-east-2:786247309603:job-completion --message "Target Machine job $AWS_BATCH_JOB_ID complete"

