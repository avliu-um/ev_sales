import os
from scraper_util_avliu.util import read_from_sqs

queue_id = os.environ.get('sqs_queue_id')

message = read_from_sqs(queue_id)

platform = message['platform']
url = message['url']

print(f'platform: {platform}, url: {url}')

if platform == 'ebay':
	from ebay import get_data
elif platform == 'kbb':
	from kbb import get_data
elif message.platform == 'craigslist':
	from craigslist import get_data
else:
	print("error things because we're sad")
	raise NotImplementedError

get_data.get_data(url)
