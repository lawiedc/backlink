#!/usr/local/bin/python3

## backlink.py ##

# For The Zone and M/C Reviews
# - check if in wayback machine ( https://archive.org/help/wayback_api.php )
# - if yes, update url
# - if no, make a note that this needs to be regenerated on hoopoes.com
import sys
print(sys.path)

import mysql.connector
from mysql.connector import Error

core_query = """SELECT 
    concat( 
      'http://archive.org/wayback/available?url=',
        link,
        '&timestamp=',
        date_format( publication_date,"%Y%m%d")
    )
    FROM `hoo_sf_data`
    where site in 'The Zone', 'M/C Reviews'
    and link not like '%web.archive.org%'
    """


# Open database
# Set up query
# Execute
# For each line of result
#  check json output from api
#  if a good url is found, update table to use this url
#  if not, create message that this is not available