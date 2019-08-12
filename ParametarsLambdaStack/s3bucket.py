import boto3
import json
s3 = boto3.resource('s3', region_name='us-east-1')

for bucket in s3.buckets.all():
    if bucket.name == 'buckettesparametars':
        for objectt in bucket.objects.all():
            content = objectt.get()['Body'].read().decode('utf-8')
            json_content = json.loads(content)
            print(json_content)
# for bucket in s3.buckets.all():
#     if bucket.name == 'buckettesparametars':
#         for objectt in bucket.objects.all():
#             print(objectt.key)