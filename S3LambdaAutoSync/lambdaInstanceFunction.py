import boto3
import pprint

ec2 = boto3.resource('ec2', region_name='us-east-1')
client = boto3.client('ssm', region_name='us-east-1')

instance_id = []
for instance in ec2.instances.all():
    if instance.state['Name'] == 'running':
        instance_id.append(instance.id)

command_id = ''
for i in instance_id:
    response = client.send_command(
        InstanceIds=[
            i,
        ],
        DocumentName='AWS-RunShellScript',
        Parameters={
            'commands': [
                'aws s3 sync s3://lambdabucket12234 /var/www/html/',       # The command to sync from bucket to an instance
                'echo "Synced on " `date` >> /var/log/mylogs.txt'
            ]
        },
    )
    command_id = response['Command']['CommandId']
    
output = client.get_command_invocation(
    CommandId=command_id,
    InstanceId=instance_id[0],
    )
pprint.pprint(output)