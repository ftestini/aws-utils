import json
import boto3

ec2_client = boto3.client('ec2')
event_bridge_client = boto3.client('events')

# This Lambda is triggered by EventBridge, every time an EC2 instance stops
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
        
        # Remove the targets from the rule
        targets = event_bridge_client.list_targets_by_rule(
            Rule='auto-stop-' + instance_id,
            EventBusName='default'
        )

        target_id = targets['Targets'][0]['Id']
        event_bridge_client.remove_targets(
            Rule='auto-stop-' + instance_id,
            EventBusName='default',
            Ids=[
                target_id
            ]
        )
        
        # Delete the rule
        response = event_bridge_client.delete_rule(
            Name='auto-stop-' + instance_id,
            EventBusName='default'
        )
        
        print(response)
    else:
        print('No tag for auto-stop found on current instance')
