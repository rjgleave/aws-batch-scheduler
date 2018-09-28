#!/bin/bash

date
echo "Args: $@"
env
echo "Starting Redshift load process"
echo "jobId: $AWS_BATCH_JOB_ID"
sleep $1
date
echo "Redshift load complete!"
