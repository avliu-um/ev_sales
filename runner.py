import os
from scraper_util_avliu.util import read_from_sqs


if __name__ == '__main__':
	service = os.environ.get('service')

	if service == 'links':
		platform = os.environ.get('platform')
		zip_code = os.environ.get('zip_code')
		radius = os.environ.get('radius')
		sqs_queue_id = os.environ.get('sqs_queue_id')

		from link_collector import LinkCollector
		lc = LinkCollector(platform=platform, zip_code=zip_code, radius=radius, sqs_queue_id=sqs_queue_id)
		lc.get_links()

	elif service == 'data':
		platform = os.environ.get('platform')
		url = os.environ.get('url')
		sqs_queue_id = os.environ.get('sqs_queue_id')

		from data_collector import DataCollector

		dc = None
		if sqs_queue_id:
			dc = DataCollector(sqs_queue_id=sqs_queue_id)
		elif platform and url:
			dc = DataCollector(platform=platform, url=url)

		dc.get_data()
	else:
		print('crying.')

