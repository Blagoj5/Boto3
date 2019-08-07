import boto3
import pprint

ec2 = boto3.resource('ec2', region_name='us-east-1')

store_keys = []
key_pair_info_iterator = ec2.key_pairs.all()
for key in key_pair_info_iterator:
    pprint.pprint(key.key_name) 
    store_keys.append(key.key_name)

# script_init = open('./httpd.sh', 'r').read()
# with open('./httpd.sh', 'r') as script_init:
instance = ec2.create_instances(
    ImageId='ami-0cfee17793b08a293',
    InstanceType='t2.micro',
    KeyName=store_keys[0],
    MaxCount=1,
    MinCount=1,
    UserData=open('./httpd.sh', 'r').read(),
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

for i in ec2.instances.all():
    if i.state['Name'] == 'running':
        pprint.pprint(f"The Instances are running with public ip {i.public_ip_address}")
    
for i in ec2.instances.all():
    if i.state['Name'] == 'terminated':
        pprint.pprint(f"The Instances are being terminated with {i.instance_id}")
