from helpers import robot, actions, respond
from flask import Flask, jsonify, request

app = Flask(__name__)

try:
  import googleclouddebugger
  googleclouddebugger.enable(
    breakpoint_enable_canary=False
  )
except ImportError:
  pass

@app.route("/api/file_upload/", methods=["POST"])
def process_request():
    
    commands = request.json.split("\n")
    new_robot = robot(None,None,None)
    message = {
        "report": ""
    }    
    report_count = 1

    for lines in commands:
        lines = lines.replace("\r", "")
        command = lines.split(" ")

        try:
            command[1] = command[1].split(",")
        except: # no second argument, not needed for some actions
            pass

        new_robot, report = actions(command, new_robot)    #attempts to execute commands, failure returns false if valid command

        if report:
            message["report"] = message["report"] + "\nReport " + str(report_count) + report
            report_count += 1

    return respond(message)

if __name__ == "__main__":
    app.run(port=8080, debug=True)