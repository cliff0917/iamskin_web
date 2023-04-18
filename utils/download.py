import os, gdown

def download_file(download_path, id, file_path):
    if not os.path.exists(download_path):
        url = f"https://drive.google.com/uc?id={id}"
        gdown.download(url, file_path, quiet=False)


def all_models(config):
    file_path = config['google_drive']["model"]["file_path"]
    download_file(config["model_path"], config['google_drive']['model']['id'], file_path)
    try:
        os.system(f"unzip {file_path} 2> /dev/null && rm {file_path} 2> /dev/null")
    except:
        pass


def secret_file(config):
    file_path = config['google_drive']["client_secret"]["file_path"]
    download_file(file_path, config['google_drive']['client_secret']['id'], file_path)