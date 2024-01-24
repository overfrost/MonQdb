#! Python3
# File takes an html of a saved page from Bluegolf
# Uses bs4 to parse the html and create two lists, one for players (ranked by finish)
# and a list of scores, also ranked by finish

# Import Beautifiul Soup
import bs4
import dbFunctions
import numpy as np
import pandas as pd

connection = dbFunctions.create_db_connection('MonQ.db')

c = connection.cursor()

c.execute('DROP TABLE IF EXISTS FarmersPreQ12024')

dbFunctions.dbclose(connection)