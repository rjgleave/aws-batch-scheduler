import json
import boto3

import logging
# Initialize logger and set log level
logger = logging.getLogger()
logger.setLevel(logging.INFO)

print('Loading send_sns function...')
sns = boto3.client('sns')


def lambda_handler(event, context):
    # Log the received event
    #print("Received event: " + json.dumps(event, indent=2))

    # format messages
    schedule_info = '[ Schedule ID: {}  Name: {} which started: {} '.format(event['scheduleId'], event['scheduleName'], event['startDateTime'])
    restart_msg = 'If you want to restart this failed job, you will need to copy the Schedule ID and Start Date/Time.  Instructions here: {}'.format('https://github.com/rjgleave/aws-batch-universal-scheduler')
    
    if event['scheduleStatus'] == 'FAILED':
        email_message = 'So sorry, your batch schedule: {} just finished.  Status: {}.  {}'.format(schedule_info , event['scheduleStatus'], restart_msg)
    else:
        email_message = 'Hey, your batch schedule: {} just finished.  Status: {}'.format(schedule_info , event['scheduleStatus'])    
    sms_message = 'Job: {} complete. Status: {}'.format(schedule_info, event['scheduleStatus'])

    sns_arn = event['scheduleSnsTopic']
    subject = 'Batch schedule: {} {}'.format(event['scheduleId'], event['scheduleStatus'])


    # Send message
    response = sns.publish(
        TargetArn=sns_arn,
        Message=json.dumps({'default': json.dumps(email_message),
                            'sms': json.dumps(sms_message),
                            'email': json.dumps(email_message)}),
        Subject=subject,
        MessageStructure='json'
    )

    logger.info(response)
    print('SNS function complete')
    print("Returned event: " + json.dumps(event, indent=2))
    return event