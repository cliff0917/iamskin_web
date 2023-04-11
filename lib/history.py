from flask import request, json

import globals
from lib import database

def serve(server):
    @server.route("/History", methods=["POST"])
    def get_history():
        uid = request.form.get('uid')
        data = database.get_history(uid)

        # Json response format.
        response = json.jsonify(
            [
                {
                    "type": data[i][0],
                    "upload_time": data[i][1],
                    "fine_name": data[i][2]
                }
                for i in range(len(data))
            ]
        )
        return response
    
    return server