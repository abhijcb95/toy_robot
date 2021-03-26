# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python38_app]
# [START gae_python3_app]

from uuid import uuid4

from flask import Flask, make_response, request, jsonify, request, render_template
from google.cloud import firestore


app = Flask(__name__)
db = firestore.Client()
sessions = db.collection('sessions')


@firestore.transactional
def get_session_data(transaction, session_id):
    """ Looks up (or creates) the session with the given session_id.
        Creates a random session_id if none is provided. Increments
        the number of views in this session. Updates are done in a
        transaction to make sure no saved increments are overwritten.
    """
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

    template = render_template("index.html", session_id = session["session_id"])
    resp = make_response(template)
    resp.set_cookie('session_id', session['session_id'], httponly=True)
    return resp


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080)

# [END gae_python3_app]
# [END gae_python38_app]
