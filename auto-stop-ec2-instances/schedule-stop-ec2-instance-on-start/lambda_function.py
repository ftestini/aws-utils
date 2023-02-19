import json
import boto3
import datetime

ec2_client = boto3.client('ec2')
event_bridge_client = boto3.client('events')
ssm = boto3.client('ssm')
# This Lambda is triggered by EventBridge, every time an EC2 instance starts
def lambda_handler(event, context):
    # Get the instance_id from the input
    instance_id = event['detail']['instance-id']
    
    # Read the instance's tags
    response = ec2_client.describe_tags(
    Filters=[
        {
            'Name': 'resource-id',
            'Values': [
                instance_id,
            ],
        },
    ],
    )
    
    # Search the "auto-stop" tag
    tags = response['Tags']
    behaviour_found = any(tag['Key'] == 'behaviour' and tag['Value'] == 'auto-stop' for tag in tags)
    
    if behaviour_found:
        auto_stop_window_parameter = ssm.get_parameter(Name='AutoStopWindow', WithDecryption=True)
        auto_stop_window = int(auto_stop_window_parameter['Parameter']['Value'])
        print('Auto stop window: %s' % str(auto_stop_window))

        # Create the scheduled expression
        schedule_expression = "cron({} {} {} {} ? {})".format(
            (datetime.datetime.now() + datetime.timedelta(hours=auto_stop_window)).minute,
            (datetime.datetime.now() + datetime.timedelta(hours=auto_stop_window)).hour,
            (datetime.datetime.now() + datetime.timedelta(hours=auto_stop_window)).day,
            (datetime.datetime.now() + datetime.timedelta(hours=auto_stop_window)).month,
            (datetime.datetime.now() + datetime.timedelta(hours=auto_stop_window)).year
        )
        
        # Create the new rule
        rule = event_bridge_client.put_rule(
            Name='auto-stop-' + instance_id,
            ScheduleExpression=schedule_expression,
            State='ENABLED',
            EventBusName='default'
        )
        print('Rule created: %s' % str(rule))
        
        # Associate the target passing a constant input
        aws_account_id = context.invoked_function_arn.split(":")[4]
        hibernation_enabled_parameter = ssm.get_parameter(Name='AutoStopHibernate', WithDecryption=True)
        hibernation_enabled = hibernation_enabled_parameter['Parameter']['Value']
        print('Hibernate: %s' % str(hibernation_enabled))

        target = event_bridge_client.put_targets(
                Rule='auto-stop-' + instance_id,
                EventBusName='default',
                Targets=[
                    {
                        "Id": "Lambda",
                        "Arn": "arn:aws:lambda:eu-south-1:%s:function:stop-ec2-instance" % aws_account_id,
                        "Input": '{"instance_id": "%s", "hibernate": "%s"}' % (instance_id, hibernation_enabled)
                    }
                ]
            )
        
        print('Target created: %s' % str(target))
        print('Rule successfully configured')
    else:
        print('No tag for auto-stop found on current instance')
