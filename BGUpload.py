#!Python3
# File contains fuctions to upload golf events from html to a sqlite3 db
# to use these functions, import the file as bg
# You must also path to the target event in BlueGolf, and save the leaderboard page as an html file
# to use the pandas stats upload functon you must path to the course, complete course stats page and save the html
# These functions target locallay saved html, not urls, and parse the data using Beautiful Soup
# bs4 creates and pandas will extract the relevant data and upload it to your target db

# Import Beautifiul Soup
import bs4
import dbFunctions as db
import pandas as pd

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
    path = str(Event)[:event_type]+'/'+str(Event)+'.html'
    # Open the target html file
    workFile = open(path)
    # Create a parse using the html5lib parser
    curSoup = bs4.BeautifulSoup(workFile.read(), 'html5lib')
    # Create blank lists that will store the relevant data once scraped
    pos = []
    players = []
    scores = []

    # Scrape the player data from the html file
    player_data = curSoup('span', class_='d-none d-md-inline')
    # Iterate over the scraped player data and extract the text from each tag
    # then place the text into the [plpayers] list
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
    pos_wd_data = curSoup('td', string=['WD','NC','DNF','NS'])
    # Iterate over the items in the [pos_wd] list and extract the text from the tag
    for i in range(len(pos_wd_data)):
        pos_wd.append(pos_wd_data[1].text.strip())
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

    # Combine lists into a 'leaderboard' list with grouped info by row
    leaderboard = []
    for i in range(len(players)):
        leaderboard.append((pos[i], players[i], scores[i]))
    # Create the table in the db
    db.createTable(connection, Event)
    # Upload to the table in the db
    db.list_to_table(connection, Event, leaderboard)
    print(f'{Event} leaderboard has been uploaded to the db')

    # Close the db connection
    db.dbclose(connection)

def pandasStatsUpload(Event):
    # Connect to the db
    connection = db.create_db_connection('MonQ.db')
    # Determine if the event is a PreQ or a MonQ, select the correct type
    type1 = 'MonQ'
    if type1 in str(Event):
        event_type = -4
    else:
        event_type = -5
    # Use pandas to read the table html and create a list of the dataframes on the page
    df = pd.read_html(str(Event)[:event_type]+'/'+str(Event)+'Stats.html', index_col=0, header=0)
    
    # Create a blank list to house the information
    stats = df[0]
    # Correct the column names from the html
    stats.rename(columns={'EAGLESEGL':'EAGLES', 'BIRDIESBRD':'BIRDIES','PARSPAR':'PARS','BOGEYSBOG':'BOGEYS','D BOGEYSDBL':'D BOGEYS'}, inplace=True)
    # Adjust the list so the hole is the index column
    stats = stats[:-1]
    # Upload to the database
    stats.to_sql(f'{Event}Stats',connection, if_exists='replace')
    print(f'{Event}Stats have been uploaded to the db')

    # Close the db connection
    db.dbclose(connection)

def eventTOCSV(Event):
    # Check if the event is a MonQ of PreQ. Set the correct type, which is used to set the path
    type1 = 'MonQ'
    if type1 in str(Event):
        event_type = -4
    else:
        event_type = -5
    # Set the path for the target html file
    path = str(Event)[:event_type]+'/'+str(Event)+'.html'
    # Open the target html file
    workFile = open(path)
    # Create a parse using the html5lib parser
    curSoup = bs4.BeautifulSoup(workFile.read(), 'html5lib')
    # Create blank lists that will store the relevant data once scraped
    pos = []
    players = []
    scores = []

    # Scrape the player data from the html file
    player_data = curSoup('span', class_='d-none d-md-inline')
    # Iterate over the scraped player data and extract the text from each tag
    # then place the text into the [plpayers] list
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
    pos_wd_data = curSoup('td', string=['WD','NC','DNF','NS'])
    # Iterate over the items in the [pos_wd] list and extract the text from the tag
    for i in range(len(pos_wd_data)):
        pos_wd.append(pos_wd_data[1].text.strip())
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

    # Combine lists into a 'leaderboard' list with grouped info by row
    leaderboard = []
    for i in range(len(players)):
        leaderboard.append((pos[i], players[i], scores[i]))
    # Create a df from the leaderboard list
    df = pd.DataFrame(leaderboard, columns=['Pos', 'Player', 'Score'])
    # Create a csv file from the leaderboard.
    csvPath = str(Event)[:event_type]+'/'+str(Event)+'.csv'
    print(csvPath)
    df.to_csv(csvPath, index=False)
    print(f'{Event} leaderboard has been converted to a csv.')

