import json
import os

from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename

import CourseParser
import DataRetrieval

app = Flask(__name__)
api = Api(app)
CORS(app)

# App config foe transcript upload
app.config["TRANSCRIPT_UPLOAD"] = "./transcripts"
app.config["ALLOWED_EXTENSIONS"] = ["TXT"]


def allowed_file(filename):
    if "." not in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_EXTENSIONS"]:
        return True
    else:
        return False


class prereqsTree(Resource):
    def get(self, course):
        return json.loads(DataRetrieval.prereqTree(course))


class courseDirectory(Resource):
    def get(self):
        return json.loads(DataRetrieval.courseDirectory())


class courseInfo(Resource):
    def get(self, course):
        return json.loads(DataRetrieval.courseInfo(course))


class getCourses(Resource):
    def get(self, withIDs):
        return json.loads(DataRetrieval.getAllCourses(withIDs))


class uploadedTranscript(Resource):
    def post(self):
        if 'transcript' in request.files:
            file = request.files['transcript']
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["TRANSCRIPT_UPLOAD"], filename))
                # Call the parse function
                return json.loads(CourseParser.courseParse(filename))
            else:
                return json.loads(json.dumps('ERROR'))
        else:
            return json.loads(json.dumps('ERROR'))


class contentLocks(Resource):
    def get(self, content):
        return json.loads(DataRetrieval.getContentLockStatus(content))

    def post(self, content):
        return json.loads(DataRetrieval.setContentLockStatus(content))


class dataLoad(Resource):
    def get(self):
        return json.loads(DataRetrieval.dataLoad())


class saveRecord(Resource):
    def post(self):
        incomingData = request.get_json()
        if incomingData['type'] == 'message':
            return json.loads(DataRetrieval.saveMessage(incomingData['data']))
        else:
            return json.loads(DataRetrieval.saveNote(incomingData['data']))


class saveComment(Resource):
    def post(self):
        newComment = request.get_json()
        return json.loads(DataRetrieval.saveComment(newComment['comment']))


class editComment(Resource):
    def post(self):
        comment = request.get_json()
        return json.loads(DataRetrieval.editComment(comment['comment']))


api.add_resource(prereqsTree, '/DataRetrieval/<course>')
api.add_resource(courseDirectory, '/DataRetrieval/directory')
api.add_resource(courseInfo, '/DataRetrieval/courseInfo/<course>')
api.add_resource(getCourses, '/DataRetrieval/courses/<withIDs>')
api.add_resource(uploadedTranscript, '/DataPosting/transcript')
api.add_resource(contentLocks, '/DataRetrieval/contentLocks/<content>')
api.add_resource(dataLoad, '/DataRetrieval/dataLoad')
api.add_resource(saveRecord, '/DataPosting/record')
api.add_resource(saveComment, '/DataPosting/comment')
api.add_resource(editComment, '/DataPosting/editcomment')

if __name__ == '__main__':
    app.run()
