import boto3
from moto import mock_kinesis
import credentials
import sys
from botocore.exceptions import ClientError

aws_key_id = "XXXXXXXXXXXX"
aws_key = "XXXXXXXXXXXXXXX"

def create_stream(client, stream_name):
    return client.create_delivery_stream(DeliveryStreamName=stream_name ,S3DestinationConfiguration={'RoleARN': 'arn:aws:iam::406659499942:role/firehose_delivery_role','BucketARN': 'arn:aws:s3:::trends-project-team2','Prefix': stream_name+'/'})

def main(search_name):
    stream_name = search_name[0]
    client = boto3.client('firehose', region_name='us-east-2', aws_access_key_id=aws_key_id,aws_secret_access_key=aws_key)

    try:
        create_stream(client,stream_name)
        print 'Creating Kinesis stream... Please wait...'
        time.sleep(60)
    except:
        pass

    stream_status = client.describe_delivery_stream(DeliveryStreamName=stream_name)
    if stream_status['DeliveryStreamDescription']['DeliveryStreamStatus'] == 'ACTIVE':
        print "\n ==== KINESES ONLINE ===="
 
if __name__ == '__main__':
    main(sys.arg[1:])
    
 #REEAhMis
