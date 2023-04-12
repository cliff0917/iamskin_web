from lib import history, login, comments, external_login

def serve(server):
    server = history.serve(server)
    server = history.update(server)
    server = login.serve(server)
    server = comments.serve(server)
    server = external_login.serve(server)
    return server