# deploys the frontend webpage for toy-robot using flask framework
# calls the cli & file_upload api using the url and api_keys for security

from uuid import uuid4

from flask import Flask, make_response, request, jsonify, request, render_template
from google.cloud import firestore
import os, requests

api_key = os.environ.get("API_KEY")
app = Flask(__name__)
db = firestore.Client()
sessions = db.collection('sessions')


@firestore.transactional
def get_session_data(transaction, session_id):

    if session_id is None:
        session_id = str(uuid4())   # Random, unique identifier

    doc_ref = sessions.document(document_id=session_id)
    doc = doc_ref.get(transaction=transaction)
    if doc.exists:
        session = doc.to_dict()
    else:
        session = {
            "x": None,
            "y": None,
            "direction": None
        }
        
    transaction.set(doc_ref, session)

    session['session_id'] = session_id
    return session


@app.route('/', methods=['GET'])
def home():
    
    transaction = db.transaction()
    session = get_session_data(transaction, request.cookies.get('session_id'))

    template = render_template("index.html", session_id = session["session_id"], api_key=api_key)
    resp = make_response(template)
    resp.set_cookie('session_id', session['session_id'], httponly=True)
    return resp

@app.route(f"/api/cli/{api_key}/<api_uri>", methods=["GET"])
def cli_commands(api_uri):

    url = f"http://toy-robot-cli-svc.production.svc.cluster.local/api/cli/{api_key}/{api_uri}"
    cli_response = requests.get(url)

    return cli_response


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)

