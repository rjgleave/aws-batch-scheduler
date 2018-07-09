
# ======================================================
# RUNNING REMOTE COMMANDS ==============================
# ======================================================


# --Example 2 --- Running PROCESSES (ps aux)
# Step 1: send a simple command to a single instance to to provide information about the currently running processes 
# on the instance.  It will only return a command ID, which you send to the next command 
# below to retrieve the results.   NOTE: specifying JSON as the output will make reading it easier.
aws ssm send-command --document-name "AWS-RunShellScript" --comment "listing RUNNING PROCESSES" --instance-ids "i-06eea61bed4d5882a" --parameters commands="ps aux" --region us-east-2 --output json
# Step 2: returns the result of the command above
aws ssm list-command-invocations --command-id "987f5667-0e17-44ef-bdf0-7c413b312555" --details

## run both commands simultaneously on a remote machine.. this returns the python version on a remote target machine
sh_command_id=$(aws ssm send-command --document-name "AWS-RunShellScript" --comment "listing RUNNING PROCESSES for a TARGET machine tag" --targets Key=tag:"targetID",Values="Instance-0001" --parameters commands="ps aux" --region us-east-2 --output text --query "Command.CommandId") sh -c 'aws ssm list-command-invocations --command-id "$sh_command_id" --details --query "CommandInvocations[].CommandPlugins[].{Status:Status,Output:Output}"'
echo $sh_command_id
sh_command_id=$(aws ssm send-command --document-name "AWS-RunShellScript" --comment "listing RUNNING PROCESSES for a TARGET machine tag" --targets Key=tag:"targetID",Values="Instance-0001" --parameters '{"commands":["#!/usr/bin/python","print \"Hello world from python\""]}' --region us-east-2 --output text --query "Command.CommandId") sh -c 'aws ssm list-command-invocations --command-id "$sh_command_id" --details --query "CommandInvocations[].CommandPlugins[].{Status:Status,Output:Output}"'

aws ssm send-command --document-name "AWS-RunShellScript" --targets Key=tag:"targetID",Values="Instance-0001" --parameters '{"commands":["#!/usr/bin/python","print \"Hello world from python\""]}' --notification-config "NotificationArn=arn:aws:sns:us-east-2:786247309603:job-completion,NotificationEvents=All,NotificationType=Command"  --service-role-arn arn:aws:iam::786247309603:role/batchjob-role-rjg --region us-east-2 --output json

aws ssm send-command --document-name "AWS-RunShellScript" --targets Key=tag:"targetID",Values="Instance-0001" --parameters '{"commands":["#!/usr/local/bin/job-simulator.sh"]}' --notification-config "NotificationArn=arn:aws:sns:us-east-2:786247309603:job-completion,NotificationEvents=All,NotificationType=Command"  --service-role-arn arn:aws:iam::786247309603:role/batchjob-role-rjg --region us-east-2 --output json

aws ssm send-command --document-name "AWS-RunShellScript" --targets Key=tag:"targetID",Values="Instance-0001" --parameters commands="job-simulator.sh" --notification-config "NotificationArn=arn:aws:sns:us-east-2:786247309603:job-completion,NotificationEvents=All,NotificationType=Command"  --service-role-arn arn:aws:iam::786247309603:role/batchjob-role-rjg --region us-east-2 --output json
"sh","-c",'aws ssm send-command --document-name "AWS-RunShellScript" --targets Key=tag:"targetID",Values="Instance-0001" --parameters commands="job-simulator" --notification-config "NotificationArn=arn:aws:sns:us-east-2:786247309603:job-completion,NotificationEvents=All,NotificationType=Command"  --service-role-arn arn:aws:iam::786247309603:role/batchjob-role-rjg --region us-east-2 --output json'