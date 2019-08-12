import boto3
import json

cf = boto3.client('cloudformation', region_name='us-east-1')
s3 = boto3.resource('s3', region_name='us-east-1')

def main(stack_name, bucket):

    template_data = __read_object(bucket, 'stack.yaml')
    parameter_data = __read_object(bucket, 'parameters.json')

    params = {
        'StackName': stack_name,
        'TemplateBody': template_data,
        'Parameters': parameter_data
    }

    create = False
    try:
        if _stack_exists(stack_name):
            print(f"Deleting stack with name {stack_name}")
            response = cf.delete_stack(StackName = stack_name)
            waiter = cf.get_waiter('stack_delete_complete')
            waiter.wait(StackName=stack_name)
            create = True
        else:
            response = cf.create_stack(**params)
            print(f"Creating stack with name {stack_name}")
            waiter = cf.get_waiter('stack_create_complete')
            waiter.wait(StackName=stack_name)
            create = False
    except Exception as e:
        print(e)
    else:
        if create:
            pass
        else:
            cf.describe_stacks(StackName=response['StackId'])
        
    try:
        if create:
            print(f"Creating NEW stack with the same name")
            response = cf.create_stack(**params)
            waiter = cf.get_waiter('stack_create_complete')
            waiter.wait(StackName=stack_name)
    except Exception as e:
        print(e)
    else:
        cf.describe_stacks(StackName=response['StackId'])

def __read_object(bucket, objectname):
    for oneobject in bucket.objects.all():
        if oneobject.key == objectname:
            if objectname == 'stack.yaml':
                content = oneobject.get()['Body'].read().decode()
                cf.validate_template(TemplateBody=content)
            if objectname == 'parameters.json':
                json_content = oneobject.get()['Body'].read().decode('utf-8')
                content = json.loads(json_content)
            return content
            

def _stack_exists(stack_name):
    stacks = cf.list_stacks()['StackSummaries']
    for stack in stacks:
        if stack['StackStatus'] == 'DELETE_IN_PROGRESS':
            continue
        if stack['StackStatus'] == 'DELETE_COMPLETE':
            continue
        if stack['StackName'] == stack_name:
            return True
    return False
    

if __name__ == '__main__':
    stack_name = 'LambdaStack'
    template = ''
    parameter = ''
    for bucket in s3.buckets.all():
        if bucket.name == 'buckettesparametars':
            main(stack_name, bucket)

    