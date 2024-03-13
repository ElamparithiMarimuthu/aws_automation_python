import json
import boto3

ec2 = boto3.resource('ec2')

def lambda_handler(event, context):
    print(event)
    
    # Extract user from the event
    user = event.get('detail', {}).get('userIdentity', {}).get('userName')
    
    if user:
        # Extract instance information
        instances_set = event.get('detail', {}).get('responseElements', {}).get('instancesSet', {}).get('items', [])
        
        if instances_set:
            # Get the instance ID from the first element if instancesSet is not empty
            instance_id = instances_set[0].get('instanceId')
            if instance_id:
                # Attach a tag to the instance with owner information
                ec2.create_tags(
                    Resources=[instance_id],
                    Tags=[{'Key': 'owner', 'Value': user}]
                )
                print(f"Tag 'owner' attached to instance {instance_id} for user {user}.")
            else:
                print("No instance ID found in the event.")
        else:
            print("No instancesSet found in the event.")
    else:
        print("No user information found in the event.")
