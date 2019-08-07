import boto3
import pprint
from botocore.exceptions import ClientError


client = boto3.client('ec2', region_name='us-east-1')

key_pair=client.describe_key_pairs()['KeyPairs']
key_pair_ec2=""
for keys in key_pair:
    pprint.pprint(f"Using key pair {keys['KeyName']}")
    key_pair_ec2 = keys['KeyName']

try:
    security_group = client.create_security_group(
        Description='MySecGroup',
        GroupName='WebDMZ',
    )
except ClientError as e:
    print(f"{e}")
else:
    pprint.pprint(security_group)

security_group = client.describe_security_groups(GroupNames=['WebDMZ'])['SecurityGroups'][0]['GroupId']
pprint.pprint(f"Using {security_group}")


instance=client.run_instances(
    ImageId='ami-0cfee17793b08a293',
    InstanceType='t2.micro',
    KeyName=f'{key_pair_ec2}',
    MaxCount=1,
    MinCount=1,
    SecurityGroupIds=[
        security_group,
    ],
    TagSpecifications=[
        {
            'ResourceType': 'instance',           
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'MyECInstance'
                },
            ]
        },
    ],
)
