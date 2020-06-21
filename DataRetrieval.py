from SQL import *
import re
import json


def prereqTree(course):
    """
    This function is designed to look through the database and find all the prereqs for the desired course
    """
    # Dictionary to store all the info
    pre = {"name": course,
           "image_url": "https://seethefullpicture.ca/wp-content/uploads/2019/06/Alcon_SeeTheFullPicture_Website_1901x11252.jpg",
           "children": [{"name": "BOB",
                         "image_url": "https://seethefullpicture.ca/wp-content/uploads/2019/06/Alcon_SeeTheFullPicture_Website_1901x11252.jpg"},
                        {"name": "JUSTIN",
                         "image_url": "https://seethefullpicture.ca/wp-content/uploads/2019/06/Alcon_SeeTheFullPicture_Website_1901x11252.jpg"}]}
    # Create the db connection
    connection = createConnection()
    # Get the prereqs for the course
    prereqsD = getPrereqs(course, connection)
    # String return var
    stringTree = course + "\n"

    # Run a loop to go through all the prereqs for the C level course
    for prereqsC in prereqsD:
        if not isinstance(prereqsC, list):
            # Add in the prereqs and course into the dictionary
            preC = getPrereqs(prereqsC, connection)
            spot = prereqsD.index(prereqsC)
            stringTree += "\t" + prereqsC + "\n"
            # Inner loop to check prereqs for the B level courses
            for prereqsB in preC:
                # Check so we loop over every other item and not over the new items we added in
                if not isinstance(prereqsB, list):
                    # Add in the prereqs and course into the dictionary
                    preB = getPrereqs(prereqsB, connection)
                    spotB = preC.index(prereqsB)
                    stringTree += "\t\t" + prereqsB + "\n"
                    # Inner loop to check prereqs for the A level courses
                    for prereqsA in preB:
                        # Check so we loop over every other item and not over the new items we added in
                        if not isinstance(prereqsA, list):
                            # Add in the prereqs and course into the dictionary
                            preA = getPrereqs(prereqsA, connection)
                            spotA = preB.index(prereqsA)
                            stringTree += "\t\t\t" + prereqsA + "\n"
                            if len(preA) > 0:
                                for courseA in preA:
                                    stringTree += "\t\t\t\t" + courseA + "\n"
                            preB.insert(spotA + 1, preA)

                    preC.insert(spotB + 1, preB)
            prereqsD.insert(spot + 1, preC)

    # End the connection
    endConnection(connection)
    # Return the list
    return json.dumps(pre, indent=4, separators=(',', ': '))


def prereqData(course):
    """
    This function is designed to look through the database and find all the prereqs for the desired course
    """
    # Dictionary to store all the info
    pre = {"name": course,
           "image_url": "https://seethefullpicture.ca/wp-content/uploads/2019/06/Alcon_SeeTheFullPicture_Website_1901x11252.jpg",
           "children": []}
    # Create the db connection
    connection = createConnection()
    # Get the prereqs for the course
    prereqsD = getPrereqs(course, connection)


def getPrereqs(course, connection):
    # Search for the prereqs
    with connection:
        returnItem = searchPre(connection, course)
    # Add in the prereqs and course into the dictionary
    listOfPre = re.findall(r'[A-Z]{4}[0-9]{2}[A-Z][0-9]', returnItem)
    # Parse the prereqs into a better format
    prereqList = returnItem.replace("'", "").replace(",", "").split("and")
    finalPrereqList = []
    # Loop through the list
    for pre in prereqList:
        if pre.count("]") == 2 and pre.index("or") != -1:
            finalPrereqList[-1] += pre
        else:
            finalPrereqList.append(pre)

    return listOfPre


def courseInfo(course):
    info = {}
    # Create the db connection
    connection = createConnection()

    with connection:
        courseInformation = getInformation(connection, course)

    # End the connection
    endConnection(connection)
    # Format the string return
    info["id"] = courseInformation[0][0]
    info["desc"] = courseInformation[0][5]
    info["pre"] = courseInformation[0][6]
    info["ex"] = courseInformation[0][7]
    info["limit"] = courseInformation[0][8]
    info["breadth"] = courseInformation[0][9]
    # Get unlocked courses
    info["unlocked"] = unlockedCourses(course[0:8])
    # Get the comments for the selected course
    info["comments"] = getCourseComments(courseInformation[0][0])

    # Return JSON string
    return json.dumps(info, indent=4, separators=(',', ': '))


def courseDirectory():
    finalDir = []
    mainDir = {}
    subDir = {}
    courses = {}
    idCounter = 0
    # Create the db connection
    connection = createConnection()
    # Get the main directory to start
    directory = getDirectory(connection, 0, "")
    # Run a loop to get the sub directory
    for x in directory:
        mainDir['id'] = idCounter
        mainDir['name'] = x[1][-1]
        mainDir['children'] = []
        idCounter += 1

        subDirectory = getDirectory(connection, 1, x[0])
        # Run a loop to get the courses for each sub directory
        for y in subDirectory:
            subDir['id'] = idCounter
            subDir['name'] = y[1]
            subDir['children'] = []
            idCounter += 1

            coursesDir = getDirectory(connection, 3, y[0])
            # Add the courses
            for z in coursesDir:
                courses['id'] = idCounter
                courses['name'] = z[0]
                idCounter += 1
                subDir['children'].append(courses)
                courses = {}

            mainDir['children'].append(subDir)
            subDir = {}

        finalDir.append(mainDir)
        mainDir = {}

    # End the connection
    endConnection(connection)

    # with open('data.json', 'w', encoding='utf-8') as f:
    # json.dump(finalDir, f, ensure_ascii=False, indent=4, separators=(',', ': '))

    return json.dumps(finalDir, indent=4, separators=(',', ': '))


def getAllCourses(switch):
    """
    This method will return a list of all the courses
    """
    # Create the db connection
    connection = createConnection()
    # Get the list of all the courses
    directory = getDirectory(connection, 2, "")
    # Create the list of dictionaries with the courses
    courses = []
    index = 0
    for course in directory:
        code = re.findall(r'[A-Z]{4}[0-9]{2}[A-Z][0-9]', str(course))
        if switch == '0':
            item = {"value": code[0], "text": course[0]}
        else:
            item = {"id": index, "name": course[0]}
        courses.append(item)
        index += 1

    # End the connection
    endConnection(connection)

    return json.dumps(courses, indent=4, separators=(',', ': '))


def getContentLockStatus(content):
    """
    This method will return the status of the desired page
    """
    # Create the db connection
    connection = createConnection()
    # Get the status
    status = getContentStatus(connection, content)
    # End the connection and return status
    endConnection(connection)
    return json.dumps(status)


def setContentLockStatus(content):
    """
    This method will return the status of the desired page
    """
    # Create the db connection
    connection = createConnection()
    # Get the status
    status = getContentStatus(connection, content)
    # Flip the status
    if status[0][0] == 1:
        status = setContentStatus(connection, (0, content))
    else:
        status = setContentStatus(connection, (1, content))
    # End the connection and return status
    endConnection(connection)
    return json.dumps('Success')


def dataLoad():
    """
    This method will load all the required data on initial load of the site
    """
    dataValues = []
    convertedMessages = []
    convertedNotes = []
    convertedComments = []
    # Create the db connection
    connection = createConnection()
    # Get the page locks
    status = getContentStatus(connection, '*')
    dataValues.append(status)
    # Load up the messages
    messages = getDevMessages(connection)
    # Convert the list of list to list of objects
    for message in messages:
        convertedMessages.append({'messageTitle': message[0], 'messageBody': message[1], 'date': message[2]})
    dataValues.append(convertedMessages)
    # Load up the dev notes
    notes = getUpdateNotes(connection)
    # Convert the list of list to list of objects
    for note in notes:
        convertedNotes.append({'noteTitle': note[0], 'noteBody': note[1], 'noteType': note[2], 'Colour': note[3], 'noteDate': note[4]})
    dataValues.append(convertedNotes)
    # Load the user comments
    comments = getComments(connection, '*')
    # Convert the list of list to list of objects
    for comment in comments:
        convertedComments.append({'course': comment[2][0:8], 'comment': comment[3], 'user': comment[7], 'date': comment[8][0:comment[8].index(',')], 'flagged': comment[9], 'flaggedby': comment[10]})
    dataValues.append(convertedComments)
    # End the connection and return status
    endConnection(connection)
    return json.dumps(dataValues)


def saveMessage(message):
    """
    This method will save the posted message into the db
    """
    messageInfo = [message['messageTitle'], message['messageBody'], message['date']]
    # Create the db connection
    connection = createConnection()
    # Save the message
    success = insertMessage(connection, messageInfo)
    # End the connection and return status
    endConnection(connection)
    return json.dumps('SUCCESS')


def saveNote(note):
    """
    This method will save the published note into the db
    """
    noteInfo = [note['noteTitle'], note['noteBody'], note['noteType'], note['Colour'], note['noteDate']]
    # Create the db connection
    connection = createConnection()
    # Save the message
    success = insertNote(connection, noteInfo)
    # End the connection and return status
    endConnection(connection)
    return json.dumps('SUCCESS')


def saveComment(comment):
    """
    This method will save the comment into the db
    """
    commentData = [comment['courseid'], comment['course'], comment['comment'], 6603524, comment['recommend'], comment['difficulty'], comment['bird'], comment['user'], comment['date']]
    # Create the db connection
    connection = createConnection()
    # Save the message
    success = insertComment(connection, commentData)
    # End the connection and return status
    endConnection(connection)
    return json.dumps('SUCCESS')


def getCourseComments(courseID):
    """
    This method will get all the comments for a course
    """
    courseComments = []
    # Create the db connection
    connection = createConnection()
    # Retrieve the comments
    listOfComments = getComments(connection, courseID)
    # Convert the list of list to list of objects
    for comment in listOfComments:
        courseComments.append({'comment': comment[3], 'recommend': comment[4], 'difficulty': comment[5], 'bird': comment[6], 'user': comment[7], 'date': comment[8]})
    # End the connection and return status
    endConnection(connection)
    return courseComments


def removeOld():
    """
    This function will remove all the courses that no longer exist
    """
    # Create the db connection
    connection = createConnection()
    # Get the prereq columns
    prereqCols = getPrereqColumn(connection)
    # Lop through the list and start updating
    for prereq in prereqCols:
        temp = ""
        flag = False
        temp = prereq[1]
        # Check to see if there are any courses that no longer exist
        counter = temp.count("/(")
        if counter > 0:
            flag = True
            # Run a loop to start splicing/removing
            while counter > 0:
                oldIndex = temp.index("/(")
                newPrereq = temp[:oldIndex] + temp[oldIndex + 12:]
                temp = newPrereq
                counter -= 1
        # Additional check if necessary
        extraCounter = temp.count("(")
        if extraCounter > 0:
            flag = True
            # Run a loop to start splicing/removing
            while extraCounter > 0:
                oldIndex = temp.index("(")
                newPrereq = temp[:oldIndex] + temp[oldIndex + 11:]
                temp = newPrereq
                extraCounter -= 1
        if flag:
            # Update with the new prereq
            updatePrereq(connection, (temp, prereq[0]))


def unlockedCourses(course):
    """
    This function will return a formatted list of all the courses that has the selected course as a prereq
    """
    # Create the db connection
    connection = createConnection()
    # Get the unlocked courses
    unlocked = getUnlocked(connection, course)
    # Concat a string return
    courses = ''
    # Loop through the return
    # result = {"A": [], "B": [], "C": [], "D": []}
    for course in unlocked:
        # item = (str(course).replace("'", "").replace(",", "").replace("(", "").replace(")", ""))
        # result[item[3]].append(item)
        courses += course[0][0:8] + ', '
    endConnection(connection)
    # Return the list
    return courses[0:len(courses)-2]
