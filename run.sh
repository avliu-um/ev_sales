#!/bin/bash

echo "Service=$SERVICE"
echo "Platform=$PLATFORM"

case $SERVICE in

  'links')

    case $PLATFORM in

      echo "Zip=$ZIP_CODE"
      echo "Radius=$RADIUS"

      # TODO: edit all get_links to take zip and radius
      'ebay')
        python ./ebay/get_links.py --zip $ZIP_CODE --radius $RADIUS
      ;;

      'kbb')
        python ./kbb/get_links.py --zip $ZIP_CODE --radius $RADIUS
      ;;

      'craigslist')
        python ./craigslist/get_links.py --zip $ZIP_CODE --radius $RADIUS
      ;;

      *)
        echo 'WHAT HAVE YOU DONE :('
      ;;
    esac

  ;;

  'data')

    case $PLATFORM in

      echo "url=$URL"

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