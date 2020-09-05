#!/usr/local/bin/python3

## backlink.py ##

# For The Zone and M/C Reviews
# - check if in wayback machine ( https://archive.org/help/wayback_api.php )
# - if yes, update url
# - if no, make a note that this needs to be regenerated on hoopoes.com

# Sample code from https://pynative.com/python-mysql-database-connection/

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

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='Electronics',
                                         user='pynative',
                                         password='pynative@#29')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

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