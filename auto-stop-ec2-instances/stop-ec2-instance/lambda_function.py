import boto3
ec2 = boto3.client('ec2')

def lambda_handler(event, context):

    instance = event['instance_id']
    hibernate = bool(event['hibernate'])
    print('Stopping your instances: %s' % str(instance))
    print('Hibernate: ' + str(hibernate))
    instance = ec2.stop_instances(
        InstanceIds=[instance],
        Hibernate=hibernate
    )
    print('stopped your instances: %s' % str(instance))