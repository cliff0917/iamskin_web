from flask import request, json

import globals
from utils import database

def serve(server):
    @server.route("/Comments", methods=["POST"])
    def get_comments():
        service_type = request.form.get('service_type')
        comments = database.get_comments(service_type)

        response = json.jsonify(
            [
                {
                    "name": f'{name[0]}*****{name[-1]}',
                    "publish_time": publish_time,
                    "service_type_chinese": globals.config['chinese'][service_type]['normal'],
                    "display_output": display_output,
                    "output_url":  f"https://{globals.config['domain_name']}/assets/{service_type}/img/{predict_class}.png",
                    "rate": rate,
                    "comment": comment
                }
                for uid, name, upload_time, file_name, predict_class, display_output, publish_time, rate, comment in comments[::-1]
            ]
        )
        return response
    
    return server