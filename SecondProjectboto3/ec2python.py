import boto3
import pprint

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
    pprint.pprint(f"The policy with name PolicyEC2AccessforS3andSSM already exists ")   

waiter = clientiam.get_waiter('policy_exists')
waiter.wait(
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
        print(policy.arn)
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
    print("The Role with name RoleEC2AccessforS3andSSM already exists")

role_iterator = iam.roles.all()
MyRole = ''
for role in role_iterator:
    if role.role_name == 'RoleEC2AccessforS3andSSM':
        response = role.attach_policy(
            PolicyArn = MyPolicy
        )
        break

try:
    instance_profile = iam.create_instance_profile(
        InstanceProfileName='InstanceRoleEC2AccessforS3andSSM',
        Path='/'
    )
except Exception as e:
    print("Instance profile with name InstanceRoleEC2AccessforS3andSSM exists! {}".format(e))
else:    
    response = instance_profile.add_role(
        RoleName='RoleEC2AccessforS3andSSM'
    )

MyRole = getInstanceProfileName(iam, "InstanceRoleEC2AccessforS3andSSM")

store_keys = []
key_pair_info_iterator = ec2.key_pairs.all()
for key in key_pair_info_iterator:
    pprint.pprint(key.key_name) 
    store_keys.append(key.key_name)

instanceID = ''
check = True
for i in ec2.instances.all():
    if i.state['Name'] == 'running':
        pprint.pprint(f"There's an instance running with ip: {i.public_ip_address}")
        instanceID = i.instance_id
        check = False

if check:
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
else:
    pprint.pprint(f"Instance {instanceID} is running")

    