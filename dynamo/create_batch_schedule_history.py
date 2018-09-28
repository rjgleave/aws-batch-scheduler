from __future__ import print_function # Python 2/3 compatibility
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')


table = dynamodb.create_table(
    TableName='BatchScheduleHistory',
    KeySchema=[
        {
            'AttributeName': 'scheduleId',
            'KeyType': 'HASH'  #Partition key
        },
        {
            'AttributeName': 'startDateTime',
            'KeyType': 'RANGE'  #Sort key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'scheduleId',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'startDateTime',
            'AttributeType': 'S'
        },

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)
