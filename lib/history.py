import os
from flask import request, json

import globals
from lib import database

def serve(server):
    @server.route("/History", methods=["POST"])
    def get_history():
        uid = request.form.get('uid')
        rows = database.get_history(uid)

        # Json response format.
        response = json.jsonify(
            [
                {
                    "service_type": globals.config['chinese'][service_type]['normal'],
                    "upload_time": upload_time,
                    "upload_url": f"https://{globals.config['domain_name']}/assets/web/upload/{service_type}/{uid}/{upload_time}/{file_name}",
                    "output_url": f"https://{globals.config['domain_name']}/assets/web/predict/{service_type}/{uid}/{upload_time}/{file_name}"
                }
                for service_type, upload_time, file_name in rows
            ]
        )
        return response
    
    return server


def update(server):
    @server.route("/Update-History", methods=["POST"])
    def update_history():
        now = globals.now()
        display_output_img = request.form.get('display_output_img')
        rate = request.form.get('rate')
        comment = request.form.get('comment')
        uid = request.form.get('uid')
        service_type = request.form.get('service_type')
        upload_time = request.form.get('upload_time')

        database.update_history(display_output_img, now, rate, comment, uid, service_type, upload_time)

        response = json.jsonify(
            {'status': 'success'}
        )
        return response
    
    return server