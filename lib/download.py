import os, gdown

def get_info(config, service_type, url_id, model_name):
    url = f"https://drive.google.com/uc?id={config['model'][service_type][url_id]}"
    path = f"{config['model_path']}/{config['model'][service_type][model_name]}"
    return url, path


def download(url, path):
    if not os.path.exists(path):
        gdown.download(url, path, quiet=False)
        # print(url, path)

def build_dir(config):
    if not os.path.isdir(config['model_path']):
        os.makedirs(config['model_path'])


def all(config):
    build_dir(config) # 建立 ./models/

    for service_type, data in config['model'].items():
        url, path = get_info(config, service_type, 'cls_id', 'cls_name')
        download(url, path)

        if service_type == 'Acne':
            url, path = get_info(config, service_type, 'embedding_id', 'embedding_name')
            download(url, path)