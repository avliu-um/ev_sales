import boto3


def write_to_bucket(aws_bucket, source, dest):
    # Make sure to configure ~/.aws/configure file
    s3 = boto3.resource('s3')
    s3.Bucket(aws_bucket).upload_file(source, dest)


def test_write_s3():
    bucket = 'ev-cloud-testing'
    destination = 'test_copy/kbb_data.txt'
    write_to_bucket(bucket, "./kbb/data/data.json", destination)


if __name__ == '__main__':
    test_write_s3()
