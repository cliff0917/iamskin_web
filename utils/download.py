import os, gdown

def all_models(config):
    if not os.path.exists(config["model_path"]):
        url = f"https://drive.google.com/uc?id={config['model']['url']}"
        file_path = config["model"]["file_path"]
        gdown.download(url, file_path, quiet=False)
        os.system(f"unzip {file_path} && rm {file_path}")