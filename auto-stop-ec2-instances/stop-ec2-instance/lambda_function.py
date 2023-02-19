import boto3
ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    instance = event['instance_id']
    hibernate = event['hibernate']
    print('Stopping your instances: %s' % str(instance))
    print('Hibernate: %s' % hibernate)

    # Check if hibernation input is true
    should_hibernate = hibernate == 'True'
    if should_hibernate:
        # Check if instance can hibernate
        response = ec2.describe_instance_credit_specifications(
            InstanceIds=[instance]
        )

        credit_specifications = response['InstanceCreditSpecifications'][0]

        if credit_specifications['CpuCredits']:
            instance = ec2.stop_instances(
                InstanceIds=[instance],
                Hibernate=True
            )
            return

    # If hibernation is not required or possible, then stop instead
    instance = ec2.stop_instances(
        InstanceIds=[instance]
    )
    print('stopped your instances: %s' % str(instance))