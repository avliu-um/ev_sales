#!/bin/bash

echo "Service=$SERVICE"
echo "Platform=$PLATFORM"

case $SERVICE in

  'links')

    echo "zip_code=$ZIP_CODE"
    echo "radius=$RADIUS"

    case $PLATFORM in

      # TODO: add sqs_queue_id
      'ebay')
        python ./ebay/get_links.py --zip_code $ZIP_CODE --radius $RADIUS
      ;;

      'kbb')
        python ./kbb/get_links.py --zip_code $ZIP_CODE --radius $RADIUS
      ;;

      'craigslist')
        python ./craigslist/get_links.py --zip_code $ZIP_CODE --radius $RADIUS
      ;;

      *)
        echo 'WHAT HAVE YOU DONE :('
      ;;
    esac

  ;;

  'data')

    echo "url=$URL"

    case $PLATFORM in

      # TODO: edit all get_data files to take url as env variable
      'ebay')
        python ./ebay/get_data.py --url $URL
      ;;

      'kbb')
        python ./kbb/get_data.py --url $URL
      ;;

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