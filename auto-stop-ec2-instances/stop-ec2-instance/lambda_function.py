import boto3
ec2 = boto3.client('ec2')

def lambda_handler(event, context):

    instance = event['instance_id'];
    ec2.stop_instances(InstanceIds=[instance])
    print('stopped your instances: ' + str(instance))