import boto3
import datetime
ec2 = boto3.resource('ec2', region_name="us-east-1")
iam = boto3.resource('iam', region_name="us-east-1")

time = f'{datetime.datetime.now():%Y-%m-%d}'

for instance in ec2.instances.all():
    if instance.state['Name'] == 'running':
        if time in f'{instance.launch_time}':
            print(f"Deleting instance == instance.instance_id")
            instance.terminate()

roleName = ''
for role in iam.roles.all():
        if time in f'{role.create_date}':
            roleName = role.role_name
            
policyArn = ''
for policy in iam.policies.all():
        if time in f'{policy.create_date}':
            policyArn = policy.arn


for profile in iam.instance_profiles.all():
        if time in f'{profile.create_date}':
            print(f'Deleting profile == {profile.instance_profile_name}')
            try:
                profile.remove_role(
                    RoleName = roleName
                )
            except Exception as e:
                pass
            profile.delete()


for role in iam.roles.all():
        if time in f'{role.create_date}':
            try:
                role.detach_policy(
                    PolicyArn = policyArn
                )
            except Exception as e:
                pass
            role.delete()

for policy in iam.policies.all():
    if time in f'{policy.create_date}':
        for policyversion in policy.versions.all():
            if (policyversion.is_default_version):
                continue
            else:    
                policyversion.delete()
        print(f'Deleting policy with name {policy.policy_name}')
        policy.delete()
