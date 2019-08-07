import boto3
import pprint

iam = boto3.resource('iam', region_name='us-east-1')
iamclient = boto3.client('iam', region_name='us-east-1')

waiter = iamclient.get_waiter('policy_exists')
waiter.wait(
    PolicyArn='arn:aws:iam::251080886556:policy/PolicyEC2AccessforS3andSSM',
    WaiterConfig={
        'Delay': 2,
        'MaxAttempts': 9
    }
)

policy_iterator = iam.policies.all()
for policy in policy_iterator:
    if policy.policy_name == 'PolicyEC2AccessforS3andSSM':
        print(policy.arn)
        MyPolicy = policy.arn
        break


# response = iamclient.list_policies(
#     Scope='Local',
#     OnlyAttached=False,
#     PathPrefix='/',
# )

# for policy in response['Policies']:
#     pprint.pprint(policy(PolicyName = "S3FullAccess"))
#     pprint.pprint(f"{policy['Arn']}")