import boto3
from moto import mock_kinesis
import credentials
import sys
from botocore.exceptions import ClientError


aws_key_id = "XXXXXXXXXXXXXXXXXX"
aws_key = "XXXXXXXXXXXXXXXXXXXXXXXX"

def delete_stream(client, stream_name):
   try:
        return client.delete_delivery_stream(DeliveryStreamName=stream_name)
        print 'Successfully delete kinesis stream: {}'.format(stream_name)
   except:
        print 'Kinesis {} does not exist'.format(stream_name)

def main(stream_name):
  client = boto3.client('firehose', region_name='us-east-2',
                          aws_access_key_id = aws_key_id,
                          aws_secret_access_key= aws_key
                          ) # the region may not be needed
  delete_stream(client,stream_name)


if __name__ == '__main__':
    main(sys.argv[1])
