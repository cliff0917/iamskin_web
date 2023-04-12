from lib import history, login, comments

def serve(server):
    server = history.serve(server)
    server = login.serve(server)
    server = comments.serve(server)
    return server