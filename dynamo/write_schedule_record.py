from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('BatchSchedules')
s3 = boto3.resource('s3')

# get schedule from
schedule_file_name_s3 = 'demo_schedule.json'
schedule_folder_name =  'batch-schedules'
obj = s3.Object(schedule_folder_name, schedule_file_name_s3)
data = obj.get()['Body'].read()
schedule = json.loads(data)

try:
    # write schedule record to dynamoDB table
    response = table.put_item(
    Item= schedule
    )
    print(json.dumps(response, indent=4, cls=DecimalEncoder))
    print("PutItem succeeded:")
    print(schedule)
except Exception as e:
    print(e)
    message = 'Error writing schedule record'
    print(message)
    raise Exception(message)
