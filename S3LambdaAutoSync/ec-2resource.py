import boto3
import pprint
import time

def getInstanceProfileName(iam, Name):
    for i in iam.instance_profiles.all():
        if i.name == Name:
            return i.name


ec2 = boto3.resource('ec2', region_name='us-east-1')
iam = boto3.resource('iam', region_name='us-east-1')
clientiam = boto3.client('iam', region_name='us-east-1')
try:
    policy = iam.create_policy(
        PolicyName='PolicyEC2AccessforS3andSSM',
        Path='/',
        PolicyDocument=open('./policy.json', 'r').read(),
        Description='It gives access to EC2 to S3 and SSM service'
    )
except Exception as e:
    if '(EntityAlreadyExists)' in f'{e}':
        print("Policy with name PolicyEC2AccessforS3andSSM exists!")
    else:
        print(e)   

waiterpolicy = clientiam.get_waiter('policy_exists')
waiterpolicy.wait(
    PolicyArn='arn:aws:iam::251080886556:policy/PolicyEC2AccessforS3andSSM',
    WaiterConfig={
        'Delay': 2,
        'MaxAttempts': 9
    }
)

MyPolicy = ''
policy_iterator = iam.policies.all()
for policy in policy_iterator:
    if policy.policy_name == 'PolicyEC2AccessforS3andSSM':
        MyPolicy = policy.arn
        
try:
    role = iam.create_role(
        Path='/',
        RoleName='RoleEC2AccessforS3andSSM',
        AssumeRolePolicyDocument=open('./trustpolicy.json', 'r').read(),
        Description='It gives access to EC2 for S3 and SSM service',
        Tags=[
            {
                'Key': 'Name',
                'Value': 'EC2accessS3andSSM'
            },
        ]
    )
except Exception as e:
    if '(EntityAlreadyExists)' in f'{e}':
        print("Role with name PolicyEC2AccessforS3andSSM exists!")
    else:
        print(e) 

role_iterator = iam.roles.all()
MyRole = ''
for role in role_iterator:
    if role.role_name == 'RoleEC2AccessforS3andSSM':
        response = role.attach_policy(
            PolicyArn = MyPolicy
        )
        break

waiterRole = clientiam.get_waiter('role_exists')
waiterRole.wait(
    RoleName='RoleEC2AccessforS3andSSM',
    WaiterConfig={
        'Delay': 2,
        'MaxAttempts': 8
    }
)



try:
    instance_profile = iam.create_instance_profile(
        InstanceProfileName='InstanceRoleEC2AccessforS3andSSM',
        Path='/'
    )
except Exception as e:
    if '(EntityAlreadyExists)' in f'{e}':
        print("InstanceProfile with name InstanceRoleEC2AccessforS3andSSM exists!")
    else:
        print(e)
else:    
    response = instance_profile.add_role(
        RoleName='RoleEC2AccessforS3andSSM'
    )

MyRole = getInstanceProfileName(iam, "InstanceRoleEC2AccessforS3andSSM")

store_keys = []
key_pair_info_iterator = ec2.key_pairs.all()
for key in key_pair_info_iterator:
    store_keys.append(key.key_name)

instanceID = ''
check = True
for i in ec2.instances.all():
    if i.state['Name'] == 'running':
        pprint.pprint(f"There's an instance running with ip: {i.public_ip_address}")
        instanceID = i.instance_id
        check = False
l = 0
for i in range(2000):
    time.sleep(1)
    try:
        if check:
            print(f'Creating Instance with keyname: {store_keys[0]}')
            instance = ec2.create_instances(
                ImageId='ami-0b898040803850657',
                InstanceType='t2.micro',
                KeyName=store_keys[0],
                MaxCount=1,
                MinCount=1,
                UserData=open('./httpd.sh', 'r').read(),
                IamInstanceProfile={
                        'Name': MyRole
                    },
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
            break
        else:
            pprint.pprint(f"Instance {instanceID} is running")
            break
    except Exception as e:
        if 'InvalidParameterValue' in f'{e}':
            print(f"Waiting for the instance profile to start {l}")
            l+=1
        else:
            print(e)