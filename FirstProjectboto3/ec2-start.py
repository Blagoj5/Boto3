import boto3
import pprint


client = boto3.client('ec2', region_name='us-east-1')

instance_idd=client.describe_instances(
    Filters=[
        {
            'Name': 'tag:Name', 
            'Values': [
                'MyECInstance'
                ]
        },

    ]
)

try:
    instance_id = instance_idd['Reservations'][0]['Instances']
    ids = [] # List for to STORE Multiple IDs of running instances (if there are more)
    for ID in instance_id:
        pprint.pprint(f"These are the stopped ec2-Instances IDs {ID['InstanceId']}")
        ids.append(ID['InstanceId'])
except Exception as e:
    pprint.pprint("The instances are running")
else:
    ec2ID = ids[0]  # The id of the first instance

try:
    response = client.start_instances(
        InstanceIds=[
            ec2ID,
        ],
    )
except NameError as e:
    pass
except Exception as e:
    pprint.pprint(e)
else:
    pprint.pprint(f"The Instace with ID {ec2ID} has been started")
    pprint.pprint(response)
