import bs4
import pandas as pd
import dbFunctions as db

# This function created an overall list of all PreQ players from the db
# you must pass the function the total number of PreQ events, as well as the name of the event (the SQL table name)
# For ex, for the 2023 Farmers you would pass preQlist(8, 'FarmersPreQ')

def preQlist(NoOfQ, event, year):
    # Connect to the database
    conn = db.create_db_connection('MonQ.db')
    # Create the list of players list
    preQplayerslist = []
    # Create the actual PreQ players list
    preQplayers = []
    # Switch the MonQ entered into a PreQ
    eventPreQ = str(event).replace('MonQ','PreQ')
    # Search the db for tables that correspond to the event and PreQ in NoOfQ, and return the list of players qith qual = yes
    for i in range(1, NoOfQ+1):
        query = f"""
        SELECT Player
        FROM {eventPreQ}{i}{year}
        WHERE Qual = 'yes'
        """
        results = db.read_query(conn, query)
        # Append the results to the list of lists
        preQplayerslist.append(results)
    print(preQplayerslist)
    # Close the connection to the db    
    db.dbclose(conn)
    # Iterate over the list of lists, and add each entry to the acutal players list
    for x in range(NoOfQ):
        for i in range(len(preQplayerslist[x])):
            preQplayers.append(preQplayerslist[x][i][0])
    print('Total PreQ Players', len(preQplayers), preQplayers[0])

    

preQlist(7, 'FarmersMonQ', '2024')