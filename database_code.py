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

    #user input data
    data_score = (username, int(user_score))

    #try/catch to insert user and score, prints error if username is already in use (username is primary key in table) and allows for overwriting of existing score
    try:
        cursor.execute(add_score, data_score)
        connection.commit()
        print("\nUsername & score successfully added!\n")
        ans = "yes"
    except:
        print("\nError: username already in use!\n")
        print("\nWould you like to overwrite past score for player: ", username, "? (yes/no)", sep = '')
        ans = input()

        valid = 1
        while valid != 0:
            if ans.lower() == "yes":
                updateScore(username, user_score)
                valid = 0
            elif ans.lower() == "no":
                newName = input("\nEnter a new player name: ")
                addScore(newName, user_score)
                valid = 0
            else:
                print("Error: invalid input")
                valid = 1
        
def updateScore(username, user_score):
    """
    Updates user game score for already created users
    """
    #sql statement to update leaderboard table at specified username
    update_score = ("UPDATE leaderboard "
                    "SET score = %s "
                    "WHERE username = %s")

    #user input data
    data_score = (int(user_score), username)
    
    #try/catch to update user score if they want to overwrite an old user score (username is already in table but want to update that score)
    try:
        cursor.execute(update_score, data_score)
        connection.commit()
        print("\nUser score successfully updated!\n")
    except:
        print("\nError: user score not updated!\n")

def connectDB(username, passwd, h, db):
    """
    Connects game client to the database for leaderboard access
    """
    return mysql.connector.connect(user=username, password=passwd, host=h, database=db)


#creates connection to database for Flappy Jay (replace user, password, host, and database once finalized server is up and running)
#usr = 'flappy_jay'
#pwd = 'software'
#h = '127.0.0.1'
#db = 'flappy_jay'
#connection = connectDB(usr, pwd, h, db)

#connects to school server
usr = 'wolfea'
pwd = 'wolfea'
h = '172.16.86.208'
db = 'FlappyJay'
connection = connectDB(usr, pwd, h, db)

#creates cursor 
cursor = connection.cursor()

#prompt user to enter player name after finishing game
username = input("Enter player name: ")

#*************************************************************************
#eventually change this score to get score from game environment directly
#*************************************************************************
score = 75

#add user and score to leaderboard
addScore(username, score)

#can use to reset leaderboard
#clearLeaderboard()


#close cursor and database connection
cursor.close()
connection.close()
