#!/usr/bin/python3

## backlink.py ##

# For The Zone and M/C Reviews
# - check if in wayback machine ( https://archive.org/help/wayback_api.php )
# - if yes, update url
# - if no, make a note that this needs to be regenerated on hoopoes.com

# Sample code from https://pynative.com/python-mysql-database-connection/

from myauth import *

import urllib.request
import json
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
    where link not like '%web.archive.org%'
    and ( link like '%zone-sf%' or '%media-culture%' )
    """

try:
    connection = mysql.connector.connect(host = dbhost,
                                         database = dbname,
                                         user = dbuser,
                                         password = dbpw )
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute(core_query)
        #records = cursor.fetchall()
        #for row in records:  ## note may need to switch to row[0] here
        for row in cursor.fetchone():
            with urllib.request.urlopen(row) as response:
                jsonreturn = json.loads(response.read())
                if jsonreturn["archived_snapshots"]["closest"]["available"] :
                    print(jsonreturn["archived_snapshots"]["closest"]["url"])
                else:
                    print("Could not find a match for ", row)

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed"

)

# Open database
# Set up query
# Execute
# For each line of result
#  check json output from api
#  if a good url is found, update table to use this url
#  if not, create message that this is not available
