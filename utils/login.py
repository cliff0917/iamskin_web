import os
import pathlib
import requests
import google.auth.transport.requests
from flask import session, abort, redirect, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol

import globals, database

def serve(server):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    client_secrets_file = 'assets/client_secret.json'
    client_secrets = globals.read_json(client_secrets_file)
    GOOGLE_CLIENT_ID = client_secrets["web"]["client_id"]

    flow = Flow.from_client_secrets_file(
        client_secrets_file=client_secrets_file,
        scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
        redirect_uri=client_secrets["web"]["redirect_uris"][0]
    )

    @server.route("/login")
    def login():
        authorization_url, state = flow.authorization_url()
        session["state"] = state
        return redirect(authorization_url)

    @server.route("/callback")
    def callback():
        flow.fetch_token(authorization_response=request.url)

        if not session["state"] == request.args["state"]:
            abort(500)  # State does not match!

        credentials = flow.credentials
        request_session = requests.session()
        cached_session = cachecontrol.CacheControl(request_session)
        token_request = google.auth.transport.requests.Request(session=cached_session)

        id_info = id_token.verify_oauth2_token(
            id_token=credentials._id_token,
            request=token_request,
            audience=GOOGLE_CLIENT_ID
        )
        session["google_id"] = id_info.get("sub")
        session["name"] = id_info.get("name")
        session["picture"] = id_info.get("picture")
        
        info = (session["google_id"], session["name"])
        database.add_user(info)
        return redirect(session["cur_path"])
    
    return server