#!/bin/bash

date
echo "Args: $@"
env
echo "Glue job: aggregate raw data"
echo "jobId: $AWS_BATCH_JOB_ID"
sleep $1
date
echo "Glue job complete!"
