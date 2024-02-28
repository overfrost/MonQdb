# !Python3
# This is a temp file for testing code
# Working functions should be moved to another file and pushed via a new commit

# Import Beautifiul Soup
import bs4
import dbFunctions as db
import pandas as pd


# Enter the name of the event. This will corrspond to the actual file name of the html. 
# HTML file name needs to follow the format, tournament name+ type (MonQ/PreQ#)

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

    # Define the number of qualifiers. All std events get 4 qualifiers from MonQ, except WMO
    # Fro PreQ events, qualifiers vary and we need to scrape to get the number
    # Scrape the qualifiers from the html file look for event type and the number
    # Search if the event is the WMO, of so assign 3 spots
    if 'WMO' in str(Event):
        qual_spots = 3
    # Search if a normal MonQ, if so assign 4 spots    
    elif type1 in str(Event):
        qual_spots = 4
    # If not WMO or MonQ, it is a PreQ, and we need to scrape the html for the qual spots. Scrape and assign
    else:
        qual_spots_res = curSoup('span', attrs={"style": "font-weight: normal;"})
        qual_spots_string = qual_spots_res[0].text
        qual_spots = qual_spots_string[qual_spots_string.find('(')+1:qual_spots_string.find(')')]


    for i in range(len(players)):
        if 'T' in pos[i]:
            pos_strip = pos[i][1:]
        else:
            pos_strip = pos[i]

        if pos[i] == 'WD' or pos[i] == 'NC' or pos[i] == 'NS':
            qual.append('no')
        elif int(pos_strip) <= int(qual_spots):
            qual.append('yes')
        else:
            qual.append('no')  


    
    """
    for i in range(len(players)):
        if pos[i] <= int(qual_spots)-1:
            qual.append('yes')
        else:
            qual.append('no')

    """

eventUpload(event)
    