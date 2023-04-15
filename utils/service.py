from utils import skin, nail, acne, tongue, line

def serve(server, config):
    server = skin.get_post(server)
    server = nail.get_post(server)
    server = acne.get_post(server)
    server = tongue.get_post(server)
    server = line.get_post(server, config)
    return server