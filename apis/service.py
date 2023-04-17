from apis import skin, nail, acne, tongue, history, comments, external_login

def serve(server, config):
    server = history.serve(server)
    server = comments.serve(server)
    server = external_login.serve(server)
    server = skin.get_post(server)
    server = nail.get_post(server)
    server = acne.get_post(server)
    server = tongue.get_post(server)
    return server