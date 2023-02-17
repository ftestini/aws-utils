# Automatically turn off your EC2 instances

EC2 instances are Virtual Machines in AWS Cloud, that acts as remote servers.

They could also be used as a simple development environment, and in this case they doesn't need to run all time.

Typically, in these cases companies plans a start / stop schedule of the instances, using EventBridge and Lambda functions in a manner that is also officially documented by [AWS](https://aws.amazon.com/it/premiumsupport/knowledge-center/start-stop-lambda-eventbridge/)

But what should we do if we want to start the instances from the EC2 console whenever we want, making sure that they are turned off after a certain period of time?

We can also use EventBridge and Lambda, but the implementation is a little trickier.

This CloudFormation template provides a complete solution to automatically turn off your EC2 instances, just install it by the provided [One-Click Deployment URL](https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/quickcreate?stack_name=AutoStopEC2Instances&templateURL=https://filippo-testini-aws-utils.s3.eu-south-1.amazonaws.com/auto-stop-ec2-instances/AutoStopEC2Instances.yaml), and then tag your istances that you want to automatically stop with this tag:
- Name: behaviour
- Value: auto-stop

The default window is of 4 hour, you can change it by modifying the SSM Parameter named "AutoStopWindow", that is also created with the template.

More info [here](https://filippotestini.medium.com/how-to-automate-stopping-of-an-ec2-instance-af8501968059)
