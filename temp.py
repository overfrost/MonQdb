# !Python3
# This is a temp file for testing code
# Working functions should be moved to another file and pushed via a new commit

# Import Beautifiul Soup
import bs4
import dbFunctions as db
import pandas as pd

event = input('Enter the short name of the event \'YYYYXXXMonQ\' or PreQ: ')
year = str(event)[:4]

def eventUpload(Event):
    # Connect to the db
    connection = db.create_db_connection('MonQ.db')
    # Check if the event is a MonQ of PreQ. Set the correct type, which is used to set the path
    type1 = 'MonQ'
    if type1 in str(Event):
        event_type = -4
    else:
        event_type = -5
    # Set the path for the target html file
    path = 'Tournaments'+'/'+str(Event)[4:event_type]+'/'+str(year)+'/'+str(Event)+'.html'
    # Open the target html file
    workFile = open(path)
    # Create a parse using the html5lib parser
    curSoup = bs4.BeautifulSoup(workFile.read(), 'html5lib')
    # Create blank lists that will store the relevant data once scraped
    pos = []
    players = []
    scores = []
    qual = []
 
    # Scrape the player data from the html file
    player_data = curSoup('span', class_='d-none d-md-inline')
    # Iterate over the scraped player data and extract the text from each tag
    # then place the text into the [players] list
    for i in range(2,len(player_data)-1):
        players.append(player_data[i].text.strip())

    # Scrape the position data from the html file
    pos_data = curSoup('td', class_='pos')
    # Iterate over the scraped pos data and extract the text from each tag
    # then place the text into the [pos] list
    for i in range(0,len(pos_data)):
        pos.append(pos_data[i].text.strip())
    # Create a blank list to represent the players who did not finish
    pos_wd = []
    # Scrape data from the html for the DNF players
    pos_wd_data = curSoup('td', string=['WD','NC','DNF','NS','DQ'])
    # Iterate over the items in the [pos_wd] list and extract the text from the tag
    for i in range(len(pos_wd_data)):
        pos_wd.append(pos_wd_data[i].text.strip())
    # Add the [pos_wd] list to the pos list to cover all players
    pos = pos + pos_wd

    # Scrape the score data from the html file
    score_data = curSoup('td', class_='total-strk')
    # Iterate over the score data. If the score is valid, add it to the [scores] list
    # if the score is blank (from a DNF player) set it to zero
    # Note this code also converts the scores to (int) values for data analysis
    for i in range(0,len(score_data)):
        if len(score_data[i].text) > 1:
            scores.append(int(score_data[i].text.strip()))
        else:
            scores.append(0)

    # Scrape the qualifiers from the html file
    qual_spots_res = curSoup('span', attrs={"style": "font-weight: normal;"})
    qual_spots_string = qual_spots_res[0].text
    qual_spots = qual_spots_string[qual_spots_string.find('(')+1:qual_spots_string.find(')')]
    print(qual_spots)
    
    for i in range(len(players)):
        if i <= int(qual_spots)-1:
            qual.append('yes')
        else:
            qual.append('no')
    
    # Combine lists into a 'leaderboard' list with grouped info by row
    leaderboard = []
    for i in range(len(players)):
        leaderboard.append((pos[i], players[i], scores[i], qual[i]))

    # Create a custom name for the table that includes the event and the event year
    dbtablename = str(Event)[4:]+str(year)
    # Create the table in the db
    db.createTable(connection, dbtablename)
    # Upload to the table in the db
    db.list_to_table(connection, dbtablename, leaderboard)
    print(f'{Event} leaderboard has been uploaded to the db') 

    # Close the db connection
    db.dbclose(connection)

eventUpload(event)