import mysql.connector


def clearLeaderboard():
    """
    Resets leaderboard by removing all usernames and scores
    """
    delete = ("DELETE FROM leaderboard")

    cursor.execute(delete)
    connection.commit()

def addScore(username, user_score):
    """
    Adds user and game score to leaderboard. Usernames cannot be repeated
    """
    #write sql statement to insert into leaderboard table
    add_score = ("INSERT INTO leaderboard "
               "(username, score) "
               "VALUES (%s, %s)")

    #create generic test user to insert
    data_score = (username, user_score)

    #try/catch to insert user and score, prints error if username is already in use (username is primary key in table)
    try:
        cursor.execute(add_score, data_score)
        connection.commit()
        print("\nUsername & score successfully added!\n")
    except:
        print("\nError: username already in use!\n")


#creates connection to database for Flappy Jay (replace user, password, host, and database once finalized server is up and running)
connection = mysql.connector.connect(user='flappy_jay', password='software', host='127.0.0.1', database='flappy_jay')

#creates cursor 
cursor = connection.cursor()

#set generic test user values for inserting into database
username = 'Test'
score = 100

#add user and score to leaderboard
addScore(username, score)

#can use to reset leaderboard
#clearLeaderboard()


#close cursor and database connection
cursor.close()
connection.close()
