import boto3
import pprint

s3 = boto3.resource('s3', region_name='us-east-1')

def PrintobjecsInsideS3(bucket):
    list = []
    for i in bucket.objects.all():
        pprint.pprint(i.key)
        pprint.pprint("-------------------------------------------------------------------------------")
        list.append(i.key)
    return list


def ListofObjecsInsideS3(bucket):
    list = []
    for i in bucket.objects.all():
        list.append(i.key)
    return list

# bucket_iterator = s3.buckets.all()
# for bucket in bucket_iterator:
#     print(f"BUCKET NAME: {bucket.name}")
#     PrintobjecsInsideS3(bucket)
