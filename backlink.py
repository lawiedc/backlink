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


# Links we know are dead, idempotent form :-)
core_query = """SELECT 
    link,
    date_format( publication_date,"%Y%m%d")
    FROM hoo_sf_data
    where link not like '%web.archive.org%'
    and ( link like '%zone-sf%' or link like '%media-culture%' )
    """

update_sql = """update hoo_sf_data set link = %s where link = %s"""

try:
    connection = mysql.connector.connect(host = dbhost,
                                         database = dbname,
                                         user = dbuser,
                                         password = dbpw )
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute(core_query)
        records = cursor.fetchall()
        for row in records:  
            # Create the API url for the record
            chkurl = 'http://archive.org/wayback/available?url=' + row[0] + '&timestamp=' + row[1]
            with urllib.request.urlopen(chkurl) as response:
                jsonreturn = json.loads(response.read())
                try:
                    jsonreturn["archived_snapshots"]["closest"]["available"]
                except:
                    # State no Wayback data available
                    print("Could not find a match for ", row)
                else:
                    # Update the data
                    update_data = ( jsonreturn["archived_snapshots"]["closest"]["url"], row[0] )
                    cursor.execute(update_sql, update_data)
        connection.commit()

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()

