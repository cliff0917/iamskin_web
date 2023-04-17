from flask import request, json

from utils import database

def serve(server):
    @server.route("/External-Login", methods=["POST"])
    def external_login():
        uid = request.form.get('uid')
        name = request.form.get('name')

        info = (uid, name)
        database.add_user(info)

        # Json response format.
        response = json.jsonify(
            {'status': 'success'}
        )
        return response
    
    return server