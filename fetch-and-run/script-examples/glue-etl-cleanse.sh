#!/bin/bash

date
echo "Args: $@"
env
echo "Starting validate and cleanse ETL process"
echo "jobId: $AWS_BATCH_JOB_ID"
sleep $1
date
echo "Cleanse ETL complete!"
