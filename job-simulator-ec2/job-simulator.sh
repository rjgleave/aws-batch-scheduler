#!/bin/bash
## you can install this script on an eC2 instance to simulate a remote job -- for testing

## simple delay to simulate doing some work
delay_time=30

date
echo "This job is simulating actual work..."

echo "working... working... working..."
echo "delay time is $delay_time"
sleep $delay_time
date
echo "All Done...bye!!"

# force the region (if you like)
export AWS_DEFAULT_REGION=us-east-2

## Send email to notify job completion
aws sns publish --topic-arn arn:aws:sns:us-east-2:786247309603:job-completion --message "Job Simulator ran successfully on Target Machine"
