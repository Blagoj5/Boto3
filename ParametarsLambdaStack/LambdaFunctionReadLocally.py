import boto3
import json

cf = boto3.client('cloudformation', region_name='us-east-1')


def main(stack_name, template, parametars):

    template_data = _read_templatt(template)
    parameter_data = _read_parametars(parametars)

    params = {
        'StackName': stack_name,
        'TemplateBody': template_data,
        'Parameters': parameter_data
    }

    try:
        if _stack_exists(stack_name):
            response = cf.delete_stack(params['StackName'])
            waiter = cf.get_waiter('stack_create_complete')
            waiter.wait(StackName=stack_name)
        else:
            response = cf.create_stack(**params)
            waiter = cf.get_waiter('stack_create_complete')
            waiter.wait(StackName=stack_name)
    except Exception as e:
        print(e)
    else:
        cf.describe_stacks(StackName=response['StackId'])
        

def _read_templatt(template):
    with open(template, 'r') as file:
        data = file.read()
    cf.validate_template(TemplateBody=data)
    return data


def _read_parametars(parametars):
    with open(parametars, 'r') as file:
        data = json.load(file)
    return data


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
    main(stack_name, template, parameter)