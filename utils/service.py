from utils import skin, nail, acne, line

def serve(server, config):
    server = skin.get_post(server)
    server = nail.get_post(server)
    server = acne.get_post(server)
    server = line.get_post(server, config)
    return server
