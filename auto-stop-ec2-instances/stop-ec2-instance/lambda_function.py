import boto3
ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    instance = event['instance_id']
    print('Stopping your instances: %s' % str(instance))
    instance = ec2.stop_instances(
        InstanceIds=[instance]
    )
    print('stopped your instances: %s' % str(instance))