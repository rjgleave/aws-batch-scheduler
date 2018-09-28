#!/bin/bash

date
echo "Args: $@"
env
echo "starting conversion:  CSV to Parquet"
echo "jobId: $AWS_BATCH_JOB_ID"
sleep $1
date
echo "Parquet conversion complete!"
