from helpers import robot, actions
from flask import Flask, jsonify, request
import json
from google.cloud import firestore #, storage

app = Flask(__name__)
db = firestore.Client()     # requires GCLOUD_PROJECT environment variable to be set
sessions = db.collection('sessions')
# storage_client = storage.Client()

try:
  import googleclouddebugger
  googleclouddebugger.enable(
    breakpoint_enable_canary=False
  )
except ImportError:
  pass

@firestore.transactional
def get_session_data(transaction, session_id):
    doc_ref = sessions.document(document_id=session_id)
    doc = doc_ref.get(transaction=transaction)
    if doc.exists:
        new_robot_data = doc.to_dict()
    else:
        new_robot_data = {
                "x" : None,
                "y" : None,
                "direction": None
            }

        transaction.set(doc_ref, new_robot_data)

    new_robot = robot(new_robot_data["x"], new_robot_data["y"], new_robot_data["direction"])

    return new_robot

@firestore.transactional
def set_session_data(transaction, session_id, new_robot_data):
    doc_ref = sessions.document(document_id=session_id)
    transaction.set(doc_ref, new_robot_data)

@app.route("/api/cli/<api_uri>", methods=["GET"])
def cli_commands(api_uri):
    
    transaction = db.transaction()

    failure = False


    command = api_uri.split(" ")
    session_id = command[0]
    command = command[1:]
    try:
        command[1] = command[1].split(",")
    except: # no second argument, not needed for some actions
        pass

    new_robot = get_session_data(transaction, session_id)
    
    new_robot, failure, report = actions(command, new_robot)    #attempts to execute commands, failure returns false if valid command

    if failure:
        return jsonify(message="Invalid Command!")
        
    else:

        if report:
            return jsonify(message=report)
        
        else:

            new_robot_data = {
                "x" : new_robot.x,
                "y" : new_robot.y,
                "direction" : new_robot.direction
            }

            set_session_data(transaction, session_id, new_robot_data)    #set updated state into NoSQL db

            return jsonify(message="Command sent!")

    

# @app.route("/api/file_upload/<session_id>")
# def file_upload_commands(session_id=None):
#     bucket = storage_client.bucket("toy_robot_uploaded_instructions")     #take note of bucket name
#     bucket.blob(session_id).download_to_filename("import_instructions.txt")
    
#     # check state in NoSQL db
#     doc = db.collection(u"sessions").document(session_id)
#     if doc.get().exists:
#         new_robot_data = doc.get().to_dict()
#         new_robot = robot(new_robot_data["x"], new_robot_data["y"], new_robot_data["direction"])
#     else:
#         new_robot = False
    
#     # Execute instructions from file
#     lines = open("import_instructions.txt", "r").readlines()
#     for line in lines:
#         line = line.replace("\n","")
#         command = line.split(" ")
#         if len(command) > 1:
#             command[1] = command[1].split(",")

#         new_robot = actions(command, new_robot)
    
#     #set updated state into NoSQL db
#     doc.set({
#         "x" : new_robot.x,
#         "y" : new_robot.y,
#         "direction" : new_robot.direction
#     })

if __name__ == "__main__":
    app.run(port=8080, debug=True)