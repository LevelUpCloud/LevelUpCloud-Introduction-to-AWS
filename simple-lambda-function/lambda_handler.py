import boto3
import os

def lambda_handler(event, context):
    
    key =    event['Records'][0]['s3']['object']['key']
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    
    s3_client = boto3.client('s3')
    
    #open object from s3
    with open('/tmp/overlay.png', 'wb') as data:
        s3_client.download_fileobj(bucket_name, 'overlay.png', data)
    
    #open object from s3
    with open('/tmp/filein', 'wb') as data:
        s3_client.download_fileobj(bucket_name, key, data)
    
    os.system("convert -brightness-contrast -1x50 -scale 32x32 /tmp/filein /tmp/fileout")
    os.system("convert -composite /tmp/fileout  /tmp/overlay.png  -scale 500x500 /tmp/out")
    
    #save object to S3
    with open('/tmp/out', 'rb') as data:
        s3_client.upload_fileobj(data, os.environ['processed_bucket'], key)
    
    return