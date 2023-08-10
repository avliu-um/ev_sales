import boto3
import datetime
import os

# TODO: Abstract these functions into util


def get_log_time():
    dt = datetime.datetime.now()
    epoch = datetime.datetime.utcfromtimestamp(0)
    time = int((dt - epoch).total_seconds() * 1000.0)
    return time

def write_cloudwatch_log(message):
    client = boto3.client('logs')
    response = client.put_log_events(
        logGroupName='test_local_to_cloudwatch',
        logStreamName='test_stream',
        logEvents=[
            {
                'timestamp': get_log_time(),
                'message': message
            },
        ]
        #,sequenceToken='string'
    )
    print(f'response: {response}')

def write_to_bucket(aws_bucket, source, dest):
    # Make sure to configure ~/.aws/configure file
    s3 = boto3.resource('s3')
    s3.Bucket(aws_bucket).upload_file(source, dest)


def test_write_s3():
    bucket = 'ev-cloud-testing'
    destination = 'test_copy/kbb_data.txt'
    try:
        write_to_bucket(bucket, "./kbb/data/data.json", destination)
        write_cloudwatch_log('done!')
    except Exception as e:
        write_cloudwatch_log('error!')
        pass


if __name__ == '__main__':
    print(f'pwd: {os.getcwd()}')
    test_write_s3()
