import boto3
import pprint


client = boto3.client('ec2', region_name='us-east-1')

instance_idd=client.describe_instances()

def delete_instances(IDD):
    response = client.terminate_instances(
        InstanceIds=[
            IDD,
        ],
    )
    return response

try:
    instance_id = instance_idd['Reservations']
# List for to STORE Multiple IDs of running instances (if there are more)   
    ids = [] 
    for ID in instance_id:
        pprint.pprint(f"These are the instances that will be terminated {ID['Instances'][0]['InstanceId']}")
        ids.append(ID['Instances'][0]['InstanceId'])
except Exception as e:
    pprint.pprint("The instances are terminated")

for ec2ID in ids:
    try:
        delete_instances(ec2ID)
    except NameError as e:
        pass
    except Exception as e:
        pprint.pprint(e)
    else:
        pprint.pprint(f"The Instace with ID {ec2ID} has been terminated")
        pprint.pprint(delete_instances(ec2ID))
