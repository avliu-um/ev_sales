#!/bin/bash

echo "Service=$SERVICE"
echo "Platform=$PLATFORM"

case $SERVICE in

  'links')

    echo "zip_code=$ZIP_CODE"
    echo "radius=$RADIUS"

    case $PLATFORM in

      'ebay')
        python ./ebay/get_links.py --zip_code $ZIP_CODE --radius $RADIUS --sqs_queue_id $SQS_QUEUE_ID
      ;;

      'kbb')
        python ./kbb/get_links.py --zip_code $ZIP_CODE --radius $RADIUS --sqs_queue_id $SQS_QUEUE_ID
      ;;

      # TODO: Implement this python file
      'craigslist')
        python ./craigslist/get_links.py --zip_code $ZIP_CODE --radius $RADIUS --sqs_queue_id $SQS_QUEUE_ID
      ;;

      *)
        echo 'WHAT HAVE YOU DONE :('
      ;;
    esac

  ;;

  'data')

    echo "url=$URL"

    case $PLATFORM in

      'ebay')
        python ./ebay/get_data.py --url $URL
      ;;

      'kbb')
        python ./kbb/get_data.py --url $URL
      ;;

      # TODO: Implement this Python file
      'craigslist')
        python ./craigslist/get_data.py --url $URL
      ;;

      *)
        echo "sqs_queue_id=$SQS_QUEUE_ID"
        python ./run_data_colllector.py --sqs_queue_id $SQS_QUEUE_ID
      ;;
    esac

  ;;

  *)
    echo 'WHAT HAVE YOU DONE :('
  ;;

esac