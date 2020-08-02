import sqlite3
from sqlite3 import Error


def createConnection():
    """
    Create a database connection to the SQLite database
    """
    connection = None
    # Try connecting to the database
    try:
        connection = sqlite3.connect("UtscCourses.db")
    except Error as e:
        print(e)
    # Return the connection if available
    return connection


def endConnection(connection):
    """
    Function to close the connection when done
    """
    connection.close()


def wipeData(connection):
    """
    Function that will wipe the database and all tables
    """
    # Clear the Main Directory
    sql = 'DELETE FROM MainDirectory'
    cur = connection.cursor()
    cur.execute(sql)
    # Clear the Sub Directory
    sql = 'DELETE FROM SubDirectory'
    cur = connection.cursor()
    cur.execute(sql)
    # Clear the Course Directory
    sql = 'DELETE FROM CourseDirectory'
    cur = connection.cursor()
    cur.execute(sql)
    # Clear the sequence data
    sql = 'DELETE FROM sqlite_sequence'
    cur = connection.cursor()
    cur.execute(sql)

    connection.commit()


def insertSection(connection, value):
    """
    This function will insert course page for each Letter in the main directory
    """
    # Create the command template
    sql = ''' INSERT INTO MainDirectory(Sections) VALUES(?) '''
    cur = connection.cursor()
    # Execute the insert
    cur.execute(sql, [value])
    # Return the ID
    return cur.lastrowid


def insertSubSection(connection, mainID, value):
    """
    This function will insert each subsection for each letter into the sub directory
    """
    # Create the command template
    sql = ''' INSERT INTO SubDirectory(MainID, SubSections) VALUES(?,?) '''
    cur = connection.cursor()
    # Execute the insert
    cur.execute(sql, [mainID, value])
    # Return the ID
    return cur.lastrowid


def insertCourse(connection, subID, mainID, courseURL, name, desc, pre, exc, limit, breadth):
    """
    This function will store all the course information into the course directory
    """
    # Create the command template
    sql = ''' INSERT INTO CourseDirectory(SubID, MainID, CourseURL, Name, Description, Prerequisite, Exclusion, StudentLimit, Breadth) VALUES(?,?,?,?,?,?,?,?,?) '''
    cur = connection.cursor()
    # Execute the insert
    cur.execute(sql, [subID, mainID, courseURL, name, desc, pre, exc, limit, breadth])
    # Return the ID
    return cur.lastrowid


def searchPre(connection, course):
    """
    This function will return the prereqs for the searched course
    """
    # Create the command template
    sql = ''' SELECT Prerequisite FROM CourseDirectory WHERE name LIKE ? '''
    cur = connection.cursor()
    # Execute the query
    cur.execute(sql, ["%" + course + "%"])
    prereqs = cur.fetchone()
    # Return the prereqs
    return str(prereqs).strip('()')


def getDirectory(connection, modifier, param):
    """
    This function will return the columns requested
    """
    # Create the command template
    cur = connection.cursor()
    if modifier == 0:
        # Execute the command
        cur.execute('''SELECT ID, Sections FROM MainDirectory''')
    elif modifier == 1:
        cur.execute('''SELECT ID, SubSections FROM SubDirectory WHERE MainID=? ''', (param,))
    elif modifier == 123:
        cur.execute('''SELECT ID, SubSections FROM SubDirectory ''')
    elif modifier == 2:
        cur.execute('''SELECT Name FROM CourseDirectory''')
    else:
        cur.execute('''SELECT Name FROM CourseDirectory WHERE SubID=? ''', (param,))
    directory = cur.fetchall()
    # Return the dir
    return directory


def getInformation(connection, course):
    """
    This function will return all the information related to the course
    """
    # Create the command template
    cur = connection.cursor()
    # Execute the command
    cur.execute(''' SELECT * FROM CourseDirectory WHERE name =?''', (course,))
    information = cur.fetchall()
    # Return the info
    return information


def getPrereqColumn(connection):
    """
    This function is designed to return the prereq and ID column for all courses
    """
    # Create the command template
    cur = connection.cursor()
    # Execute the command
    cur.execute(''' SELECT ID, Prerequisite FROM CourseDirectory''')
    prereqCols = cur.fetchall()
    # Return the info
    return prereqCols


def updatePrereqCode(connection, courseCode):
    sql = ''' UPDATE CourseDirectory SET PrereqCode = ? WHERE ID = ? '''
    cur = connection.cursor()
    # Execute the insert
    cur.execute(sql, courseCode)
    connection.commit()
    # Return the ID
    return cur.lastrowid


def updatePrereq(connection, updatedPrereq):
    sql = ''' UPDATE CourseDirectory SET Prerequisite = ? WHERE ID = ? '''
    cur = connection.cursor()
    # Execute the insert
    cur.execute(sql, updatedPrereq)
    connection.commit()
    # Return the ID
    return cur.lastrowid


def getCourseID(connection, course):
    """
    This function is designed to return the courseID for the course
    """
    # Create the command template
    sql = ''' SELECT ID FROM CourseDirectory WHERE name LIKE ? '''
    cur = connection.cursor()
    # Execute the query
    cur.execute(sql, ["%" + course + "%"])
    prereqs = cur.fetchone()
    # Return the prereqs
    return str(prereqs).strip('()').strip(',')


def getSpecialCases(connection, special):
    """
    This function will return the difficult prereq cases
    """
    # Create the command template
    cur = connection.cursor()
    # Execute the command
    cur.execute(''' SELECT Prerequisite FROM CourseDirectory WHERE PrereqCode = ?''', (special,))
    specialCases = cur.fetchall()
    # Return the info
    return specialCases


def getUnlocked(connection, course):
    """
    This function will return all courses that have the course in its prereq
    """
    # Create the command template
    sql = ''' SELECT Name FROM CourseDirectory WHERE Prerequisite LIKE ? '''
    cur = connection.cursor()
    # Execute the query
    cur.execute(sql, ["%" + course + "%"])
    unlocked = cur.fetchall()
    # Return the prereqs
    return unlocked


def getContentStatus(connection, page):
    """
    This function will return the lock status of the desired page
    """
    # Create the command template
    cur = connection.cursor()
    if page == '*':
        cur.execute(''' SELECT Status FROM ContentLocks ''')
    else:
        # Execute the command
        cur.execute(''' SELECT Status FROM ContentLocks WHERE ID = ?''', (page,))
    pageStatus = cur.fetchall()
    # Return the info
    return pageStatus


def setContentStatus(connection, status):
    """
    This function will return the lock status of the desired page
    """
    sql = ''' UPDATE ContentLocks SET Status = ? WHERE ID = ? '''
    cur = connection.cursor()
    # Execute the insert
    cur.execute(sql, status)
    connection.commit()
    # Return the ID
    return cur.lastrowid


def getDevMessages(connection):
    """
    This function will return all the dev messages
    """
    # Create the command template
    cur = connection.cursor()
    cur.execute(''' SELECT Title, Body, Date FROM DevMessages ''')
    messages = cur.fetchall()
    # Return the messages
    return messages


def getUpdateNotes(connection):
    """
    This function will return all the update notes
    """
    # Create the command template
    cur = connection.cursor()
    cur.execute(''' SELECT Title, Body, Type, Colour, Date  FROM UpdateNotes ''')
    notes = cur.fetchall()
    # Return the notes
    return notes


def insertMessage(connection, message):
    """
    This function will save the message
    """
    # Create the command template
    sql = ''' INSERT INTO DevMessages(Title, Body, Date) VALUES(?,?,?) '''
    cur = connection.cursor()
    # Execute the insert
    cur.execute(sql, message)
    connection.commit()
    # Return the ID
    return cur.lastrowid


def insertNote(connection, note):
    """
    This function will save the message
    """
    # Create the command template
    sql = ''' INSERT INTO UpdateNotes(Title, Body, Type, Colour, Date) VALUES(?,?,?,?,?) '''
    cur = connection.cursor()
    # Execute the insert
    cur.execute(sql, note)
    connection.commit()
    # Return the ID
    return cur.lastrowid


def insertComment(connection, comment):
    """
    This function will insert the comment into the database
    """
    # Create the command template
    sql = ''' INSERT INTO CourseComments(CourseID, CourseName, Comment, Flagged, Recommend, Difficulty, Bird, User, Date) VALUES(?,?,?,?,?,?,?,?,?) '''
    cur = connection.cursor()
    # Execute the insert
    cur.execute(sql, comment)
    connection.commit()
    # Return the ID
    return cur.lastrowid


def getComments(connection, courseID):
    """
    This function will return a list of all the comments for a particular course
    """
    # Create the command template
    cur = connection.cursor()
    # Execute the command
    if courseID != '*':
        cur.execute(''' SELECT * FROM CourseComments WHERE CourseID = ? AND Flagged = 6603524 ''', (courseID,))
    else:
        cur.execute(''' SELECT * FROM CourseComments ''')
    comments = cur.fetchall()
    # Return the info
    return comments


def modifyComment(connection, commentID, action, user):
    """
    This function will flag or unflag a comment
    """
    # Create the command template
    cur = connection.cursor()
    # Execute the command
    if action == 1:
        cur.execute(''' UPDATE CourseComments SET Flagged = 3524433, FlaggedBy = ? WHERE ID = ?  ''', (user, commentID,))
    else:
        cur.execute(''' UPDATE CourseComments SET Flagged = 6603524, FlaggedBy = ? WHERE ID = ?  ''', (user, commentID,))
    connection.commit()
    # Return the ID
    return cur.lastrowid
