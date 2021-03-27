from helpers import robot, actions, respond
from flask import Flask, jsonify, request
from google.cloud import firestore

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

@app.route("/api/cli/<api_uri>", methods=["POST"])
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
        message = {"message": "Invalid Command!"}
        
    else:

        if report:
            message = {"message": report}
        
        else:

            new_robot_data = {
                "x" : new_robot.x,
                "y" : new_robot.y,
                "direction" : new_robot.direction
            }

            set_session_data(transaction, session_id, new_robot_data)    #set updated state into NoSQL db

            message = {"message": "Command sent!"}

    return respond(message)

if __name__ == "__main__":
    app.run(port=8080, debug=True)