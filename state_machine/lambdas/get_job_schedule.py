from __future__ import print_function

import json
import urllib
import boto3
import os
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

print('Loading get_job_schedule function')

# NOTE: YOU MUST SET UP THE REGION VARIABLE IN THE LAMBDA!
# Import Environment Variables for Lambda configuration
REGION = os.environ['AWS_REGION']

dynamodb = boto3.resource("dynamodb", region_name=REGION)

def lambda_handler(event, context):
    # Log the received event
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the batch schedule ID and the run mode (regular or RESTART) from the state machine input document
    schedule_id = event['scheduleId']
    schedule_status = event['scheduleStatus']
    
    # if it is a re-start job, then pull the failed schedule from history
    try:
        if schedule_status == 'RESTART':
            table = dynamodb.Table('BatchScheduleHistory')
            start_date_time = event['startDateTime']
            print('start date',start_date_time)
            response = table.get_item(
                Key={
                    'scheduleId': schedule_id,
                    'startDateTime': start_date_time
                }
            )
        else:
            table = dynamodb.Table('BatchSchedules')
            response = table.get_item(
                Key={
                    'scheduleId': schedule_id
                }
            )

    except ClientError as e:
        event['scheduleMessage'] = e.response['Error']['Message']
        print(event['scheduleMessage'])
        event['scheduleStatus'] = "FAILED"
    else:
        print(response)
        if 'Item' in response:
            item = response['Item']
            print("GetItem succeeded:")
            event = item
        else:
            event['scheduleStatus'] = "FAILED"
            event['scheduleMessage'] = "Error: schedule record not found"
            print(event['scheduleMessage'])

    if schedule_status == 'RESTART':
        event['scheduleStatus'] = "RESTART"
        
    print('function complete')
    print(json.dumps(event, indent=4, cls=DecimalEncoder))
    return event