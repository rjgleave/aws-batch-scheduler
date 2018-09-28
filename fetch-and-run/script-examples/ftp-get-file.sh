#!/bin/bash

date
echo "Args: $@"
env
echo "beginning FTP file request"
echo "jobId: $AWS_BATCH_JOB_ID"
sleep $1
date
echo "FTP complete!"
