# MonQdb
Monday Qualifier Database

The goal of this project is to create a SQL database of leaderboards, statistics, course, and player information across Monday Qualifying events. 
The project will focus on the PGA Tour, Korn Ferry Tour, and LPGA tour
Most code will be written in Python 3, and commit entried to the database by reading .html files saved from webpages
Initially, this project will focus on tournamnent data hosted by BlueGolf (leaderboard and stats)
The database begins in the 2023 PGA Tour Season with the Sony Open being the first event. 
The main database is titled MonQ.db and is a sqlite3 db

Folder structure is critical in the code to open and path to the correct files. 

To run a stat report

1. Download the html files
2. run the BGUpload file to upload files to the DB
```
BGUpload.py```

