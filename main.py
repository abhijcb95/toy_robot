from helpers import robot, actions
from flask import Flask, jsonify
from google.cloud import firestore #, storage

app = Flask(__name__)
db = firestore.Client()     # requires GCLOUD_PROJECT environment variable to be set
# storage_client = storage.Client()

@app.route("/api/cli/<session_id>/<commands>")
def cli_commands(session_id=None, commands=None):
    command = commands.split("_")
    doc = db.collection(u"sessions").document(session_id)   #take note of collection name

    # check state in NoSQL db
    if doc.get().exists:
        new_robot_data = doc.get().to_dict()
        new_robot = robot(new_robot_data["x"], new_robot_data["y"], new_robot_data["direction"])
    else:
        new_robot = False
    
    if new_robot:
        new_robot = actions(command, new_robot)

        #set updated state into NoSQL db
        doc.set({
            "x" : new_robot.x,
            "y" : new_robot.y,
            "direction" : new_robot.direction
        })
        return jsonify({"message": "Command sent!"})
    else:
        return jsonify({"message": "Invalid command"})

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
    app.run(port=3000, debug=True)