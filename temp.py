# !Python3
# This is a temp file for testing code
# Working functions should be moved to another file and pushed via a new commit

# Import Beautifiul Soup
import bs4
import dbFunctions as db
import pandas as pd


data1 = input('Enter the name of the event in short [XXXMonQ] ex FarmersMonQ DO NOT INC YEAR ')
data2 = input('Enter the full name of the event [RSM Classic] ')
data3 = int(input('Enter the number of PreQ events '))
data4 = input('Enter the year of the event ')

# Find the low PreQ Name

# Create connection to the db
connection = db.create_db_connection('MonQ.db')

NoOfQ = data3
event = data1
year = data4

preQevent = str(event).replace('MonQ','PreQ')
# Create the preQ_Scores list
PreQ_list = []
for i in range(1,NoOfQ+1):
     q19 = f"""
     SELECT t1.Score
     FROM {event}{year} as t1
     INNER JOIN {preQevent}{i}{year} as t2
     ON t1.Player = t2.Player
     WHERE t1.Score > 0
     """
     results19 = db.read_query(connection, q19)

PreQ_list.append(results19)
preQ_scores = []
for i in range(NoOfQ):
     preQ_scores.append(PreQ_list[i][0][0])
     
     preQavg = sum(preQ_scores)/len(preQ_scores)


     tar = min(preQ_scores)
     preQlowName = []
     for i in range(1,NoOfQ+1):
          q3 = f"""
          SELECT t1.Player
          FROM {event}{year} as t1
          INNER JOIN {preQevent}{i}{year} as t2
          ON t1.Player = t2.Player
          WHERE t1.Score = {tar}
          """
          results3 = db.read_query(connection, q3)
          preQlowName.append(results3)

          print(preQlowName)

     db.dbclose(connection)