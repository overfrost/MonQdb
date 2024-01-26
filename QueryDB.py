import dbFunctions as db
# Query the user for the data
data1 = input('Enter the name of the event in short [XXXMonQ] ex FarmersMonQ DO NOT INC YEAR ')
data2 = input('Enter the full name of the event [RSM Classic] ')
data3 = int(input('Enter the number of PreQ events '))
data4 = input('Enter the year of the event ')

def preQlist(NoOfQ, event):
    conn = db.create_db_connection('MonQ.db')
    preQplayerslist = []
    preQplayers = []
    preQevent = str(event).replace('MonQ','PreQ')
    for i in range(1, NoOfQ+1):
        query = f"""
        SELECT Player
        FROM {preQevent}{i}
        WHERE Qual = 'yes'
        """
        results = db.read_query(conn, query)

        preQplayerslist.append(results)
    db.dbclose(conn)
    for x in range(NoOfQ):
        for i in range(len(preQplayerslist[x])):
            preQplayers.append(preQplayerslist[x][i][0])


def statReport(event, event_full, NoOfQ, year):
    # Create connection to the db
    connection = db.create_db_connection('MonQ.db')

    # Define the query to find par
    q_par = f"""
    SELECT SUM(Par)
    FROM {event}{year}Stats
    """
    # Query the stats table to find par
    par_tuple = db.read_query(connection,q_par)
    # Store the result from the par query as par
    par = par_tuple[0][0]

    # Select the four qualifiers for a MondayQ
    q1 = f"""
    SELECT Player, Score
    FROM {event}{year}
    LIMIT 4
    """

    results = db.read_query(connection, q1)

    qual1 = results[0][0] + ' ' + str(results[0][1])
    qual2 = results[1][0] + ' ' + str(results[1][1])
    qual3 = results[2][0] + ' ' + str(results[2][1])
    qual4 = results[3][0] + ' ' + str(results[3][1])

    qualifiers = [
        f'Qualifiers moving on to the {event_full}',
        qual1,
        qual2,
        qual3,
        qual4
    ]

    # Select the total number of rounds posted in the target table
    q2 = f"""
    SELECT COUNT(Player)
    FROM {event}{year}
    WHERE Score > 0
    """

    results2 = db.read_query(connection, q2)

    totalPlayers = [i[0] for i in results2]

    # Select the scoring average from the total number of rouonds
    q3 = f"""
    SELECT ROUND(AVG(Score),2)
    FROM {event}{year}
    WHERE Score > 0
    """
    score_avg = db.read_query(connection, q3)

    # Select scores under 70
    q4 = f"""
    SELECT COUNT(Score)
    FROM {event}{year}
    WHERE Score < 70 AND Score > 0
    """
    sub70 = db.read_query(connection, q4)

    # Select Scores that are par or better
    q5 = f"""
    SELECT COUNT(Score)
    FROM {event}{year}
    WHERE Score <= {par} AND Score > 0
    """
    par_or_better = db.read_query(connection, q5)

    # Select scores that are even par
    q6 = f"""
    SELECT COUNT(Score)
    FROM {event}{year}
    WHERE Score = {par}
    """
    even_par = db.read_query(connection, q6)

    # Select scores that are over par
    q7 = f"""
    SELECT COUNT(Score)
    FROM {event}{year}
    WHERE Score > {par}
    """
    over_par = db.read_query(connection, q7)

    # Select scores that are over 80
    q8 = f"""
    SELECT COUNT(Score)
    FROM {event}{year}
    WHERE Score > 80
    """
    over80 = db.read_query(connection, q8)

    # Select scores that are less than par
    q9 = f"""
    SELECT COUNT(Score)
    FROM {event}{year}
    WHERE Score < {par}
    """
    sub_par = db.read_query(connection, q9)

    # Select the medalist
    q10 = f"""
    SELECT Player, Score
    FROM {event}{year}
    LIMIT 1
    """
    medalist = db.read_query(connection, q10)
    medalist_to_par = medalist[0][1] - par
    # Select the high score
    q11 = f"""
    SELECT MAX(Score)
    FROM {event}{year}
    """
    high_round = db.read_query(connection, q11)
    High_round_to_par = high_round[0][0] - par

    # Select the Par 3 scoring average
    q12 = f"""
    SELECT ROUND(AVG(AVG),2)
    FROM {event}{year}Stats
    WHERE Par = 3
    """
    par3_avg = db.read_query(connection, q12)

    # Select the Par 4 scoring average
    q13 = f"""
    SELECT ROUND(AVG(AVG),2)
    FROM {event}{year}Stats
    WHERE Par = 4
    """
    par4_avg = db.read_query(connection, q13)

    # Select the Par 5 scoring average
    q14 = f"""
    SELECT ROUND(AVG(AVG),2)
    FROM {event}{year}Stats
    WHERE Par = 5
    """
    par5_avg = db.read_query(connection, q14)

    # Select the hardest hole
    q15 = f"""
    SELECT [Hole#], Par, AVG
    FROM {event}{year}Stats
    WHERE [TO PAR] IN (SELECT MAX([TO PAR]) FROM {event}{year}Stats)
    """
    hardest_hole_tuple = db.read_query(connection, q15)
    hardest_hole = hardest_hole_tuple[0][0]
    hardest_hole_par = hardest_hole_tuple[0][1]
    hardest_hole_avg = hardest_hole_tuple[0][2]


    # Select the easiest hole
    q16 = f"""
    SELECT [Hole#], Par, AVG
    FROM {event}{year}Stats
    WHERE [To Par] IN (SELECT MIN([To Par]) FROM {event}{year}Stats)
    """
    easiest_hole_tuple = db.read_query(connection, q16)
    easiest_hole = easiest_hole_tuple[0][0]
    easiest_hole_par = easiest_hole_tuple[0][1]
    easiest_hole_avg = easiest_hole_tuple[0][2]

    # Select the holes under par
    q17 = f"""
    SELECT COUNT([To Par])
    FROM {event}Stats
    WHERE [To Par] < 0
    """
    results17 = db.read_query(connection, q17)
    holes_under_par = results17[0][0]

    # Select the holes over par
    q18 = f"""
    SELECT COUNT([To Par])
    FROM {event}Stats
    WHERE [To Par] > 0
    """
    results18 = db.read_query(connection, q18)
    holes_over_par = results18[0][0]

    # Create the PreQPlayers list and helper lists for PreQPlayers
    PreQPlayers = []
    preQplayerslist = []
    # Change the event type (entered as MonoQ) to a PreQ so we can search PreQ data in the db
    preQevent = str(event).replace('MonQ','PreQ')
    # Search the db for tables that correspond to the event and PreQ in NoOfQ, and return the list of players with qual = yes
    for i in range(1, NoOfQ+1):
        query = f"""
        SELECT Player
        FROM {preQevent}{i}{year}
        WHERE Qual = 'yes'
        """
        results = db.read_query(connection, query)
    # Append the results to the list of lists
        preQplayerslist.append(results)
    # Iterate over the list of lists, and add each entry to the acutal players list
    for x in range(NoOfQ):
        for i in range(len(preQplayerslist[x])):
            PreQPlayers.append(preQplayerslist[x][i][0])
    
    # Create the preQ_Scores list
    PreQ_list = []
    for i in range(1,NoOfQ+1):
     q19 = f"""
     SELECT t1.Score
     FROM {event}{year} as t1
     INNER JOIN {preQevent}{i}{year} as t2
     ON t1.Player = t2.Player
     """
     results19 = db.read_query(connection, q19)

     PreQ_list.append(results19)
     preQ_scores = []
    for x in range(NoOfQ):
        for i in range(len(PreQ_list[x])):
            for z in range(len(PreQ_list[x][i])):
                preQ_scores.append(PreQ_list[x][i][z])
     
    preQavg = sum(preQ_scores)/len(preQ_scores)

    # Find the low PreQ Name
    # Remove zero scores from preQ_scores
    tempscorelist = []
    for i in range(len(preQ_scores)):
        if preQ_scores[i] != 0:
            tempscorelist.append(preQ_scores[i])
    low_preq_score = min(tempscorelist)

    preQlowNamesearch = []
    for i in range(1,NoOfQ+1):
     q20 = f"""
     SELECT t1.Player
     FROM {event}{year} as t1
     INNER JOIN {preQevent}{i}{year} as t2
     ON t1.Player = t2.Player
     WHERE t1.Score = {low_preq_score}
     """
     results20 = db.read_query(connection, q20)
     preQlowNamesearch.append(results20)
    
    preQlowName = []
    for x in range(NoOfQ):
        for i in range(len(preQlowNamesearch[x])):
            for z in range(len(preQlowNamesearch[x][i])):
                preQlowName.append(preQlowNamesearch[x][i][z])
        
    # Create the round data list
    roundData = [
        f'MondayQ {event_full} Stats',
        f'Total Rounds = {totalPlayers[0]}',
        f'Sub 70 = {sub70[0][0]}',
        f'Par or Better = {par_or_better[0][0]}',
        f'Even Par = {even_par[0][0]}',
        f'Over Par = {over_par[0][0]}',
        f'Sub Par = {sub_par[0][0]}',
        f'80+ = {over80[0][0]}',
        f'Medalist {medalist[0][1]} ({medalist_to_par}, {medalist[0][0]})',
        f'High Round {high_round[0][0]} (+{High_round_to_par})',
    ]   

    # Create the score data list
    scoreData = [
        f'Field Scoring avg {score_avg[0][0]}',
        f'Par 3 {par3_avg[0][0]}',
        f'Par 4 {par4_avg[0][0]}',
        f'Par 5 {par5_avg[0][0]}'
    ]
    # Generate the right suffix for the hardest/easiest hole
    if int(hardest_hole) == 1:
        hardest_suffix = 'st'
    elif int(hardest_hole) == 2:
        hardest_suffix = 'nd'
    elif int(hardest_hole) == 3:
        hardest_suffix = 'rd'
    else:
        hardest_suffix = 'th'

    if int(easiest_hole) == 1:
        easiest_suffix = 'st'
    elif int(easiest_hole) == 2:
        easiest_suffix = 'nd'
    elif int(easiest_hole) == 3:
        easiest_suffix = 'rd'
    else:
        easiest_suffix = 'th'
    

    # Create the hole data list
    holeData = [
        f'Toughest hole Par {hardest_hole_par} {hardest_hole}{hardest_suffix} played {hardest_hole_avg}',
        f'Easiest hole Par {easiest_hole_par} {easiest_hole}{easiest_suffix} played {easiest_hole_avg}',
        f'{holes_under_par} holes under par on avg',
        f'{holes_over_par} holes over par on avg'
    ]

    # Create the PreQ data list
    preQData = [
        f'{len(PreQPlayers)} PreQ Players average {preQavg}',
        f'Low PreQ {min(tempscorelist)} {preQlowName[0]}',
        f'High PreQ {max(preQ_scores)}'
    ]

    filename = 'Tournaments'+'/'+str(data1)[:-4]+'/'+str(year)+'/'+f'{event_full}{year}.txt'

    outfile = open(filename, 'w')
    outfile.writelines(line + '\n' for line in roundData)
    outfile.write('\n')
    outfile.writelines(line + '\n' for line in scoreData)
    outfile.write('\n')
    outfile.writelines(line + '\n' for line in preQData)
    outfile.write('\n')
    outfile.writelines(line + '\n' for line in holeData)
    outfile.write('\n')
    outfile.writelines(line + '\n' for line in qualifiers)
    outfile.close()

    print(f'{event_full} Stat Report has been generated')
    db.dbclose(connection)


# To produce a stat report, first upload all info to the db using the BGUpload functions
# Once the data is in the DB, call the statReport fuction and pass the short name to match the SQl table, the full event name, and the number of PreQualifiers
# statReport('RSMMonQ', 'RSM Classic', 4)

statReport(data1, data2, data3, data4)