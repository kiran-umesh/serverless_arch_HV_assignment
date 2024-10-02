import boto3

# Initialize EC2 resource
ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    # Stop EC2 instances with 'Auto-Stop' tag
    stop_instances()
    
    # Start EC2 instances with 'Auto-Start' tag
    start_instances()

def stop_instances():
    # Filter instances with the tag 'Auto-Stop'
    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:kiranm_auto_stop',
                'Values': ['kiranm_auto_stop']
            },
            {
                'Name': 'instance-state-name',
                'Values': ['running']  # Only stop running instances
            }
        ]
    )
    
    instances_to_stop = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances_to_stop.append(instance['InstanceId'])
    
    # Stop instances if any are found
    if instances_to_stop:
        print(f"Stopping instances: {instances_to_stop}")
        ec2.stop_instances(InstanceIds=instances_to_stop)
    else:
        print("No instances found with the 'Auto-Stop' tag that are running.")

def start_instances():
    # Filter instances with the tag 'Auto-Start'
    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:kiranm_auto_start',
                'Values': ['kiranm_auto_start']
            },
            {
                'Name': 'instance-state-name',
                'Values': ['stopped']  # Only start stopped instances
            }
        ]
    )
    
    instances_to_start = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances_to_start.append(instance['InstanceId'])
    
    # Start instances if any are found
    if instances_to_start:
        print(f"Starting instances: {instances_to_start}")
        ec2.start_instances(InstanceIds=instances_to_start)
    else:
        print("No instances found with the 'Auto-Start' tag that are stopped.")
