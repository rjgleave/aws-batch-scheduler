
# ======================================================
# Test for Passing in an Argument to run shell script
# ======================================================

## run both commands simultaneously on a remote machine.. this returns the python version on a remote target machine
aws ssm send-command --document-name "AWS-RunShellScript" --comment "listing RUNNING PROCESSES for a TARGET machine tag" --targets Key=tag:"targetID",Values="Instance-0001" --parameters commands="$1" --notification-config "NotificationArn=arn:aws:sns:us-east-2:786247309603:job-completion,NotificationEvents=All,NotificationType=Command"  --service-role-arn arn:aws:iam::786247309603:role/batchjob-role-rjg --region us-east-2 --output test

# to get the result of the above command:  aws ssm list-command-invocations --command-id "a5284cfb-a70a-4524-bf54-483c5492490f" --details
