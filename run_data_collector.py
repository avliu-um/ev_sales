import boto3
import os

queue_id = os.environ.get('sqs_queue_id')

sqs = boto3.resource('sqs')
client = sqs.Queue(f'{queue_id}')
message = client.receive_messages(MaxNumberOfMessages=1)

platform = message.platform
url = message.url

print(f'platform: {platform}, url: {url}')

# TODO: Edit all get_data files to take url as parameter
if platform == 'ebay':
	from ebay import get_data
elif platform == 'kbb':
	from kbb import get_data
elif message.platform == 'craigslist':
	from craigslist import get_data
else:
	print("error things because we're sad")
	raise NotImplementedError

get_data(url)
