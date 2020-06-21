import re
import json


def courseParse(file):
    """
    This function will parse the passed in file and return a JSON object of the courses taken by that user
    """
    courses = []
    # Open the text file
    transcript = open('./transcripts/'+str(file), 'r')
    # Run a loop to go through the file
    course = ''
    courseObj = {}
    semester = ''
    for line in transcript.readlines():
        # Get the year and semester
        if re.match(r'20[0-9][0-9]', line[:4]):
            endOfSem = line.index(' - ')
            semester = line[:endOfSem]
        if re.match(r'[A-Z]{4}[0-9]{2}[A-Z][0-9]', line[:8]):
            course = ''
            courseObj = {}
            endOfCourse = line.index('0.')
            course = line[:endOfCourse].rstrip('\n').rstrip(' ')
            courseObj['code'] = course[:8]
            courseObj['title'] = course[10:]
            courseObj['date'] = semester
            courses.append(courseObj)
        elif line[:8] == '        ':
            course += line[9:].rstrip('\n').rstrip(' ')
            # Check to see if we put the course in already
            if courseObj['code'] == course[:8]:
                courses.pop(-1)
                courseObj['code'] = course[:8]
                courseObj['title'] = course[10:]
                courseObj['date'] = semester
                courses.append(courseObj)
    # close file & Return the list of courses
    transcript.close()
    return json.dumps(courses)
