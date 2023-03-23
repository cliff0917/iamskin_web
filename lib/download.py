import os, gdown

def get_info(config, types, url_id, model_name):
    url = f"https://drive.google.com/uc?id={config['model'][types][url_id]}"
    path = f"{config['model_path']}/{config['model'][types][model_name]}"
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

    for types, data in config['model'].items():
        url, path = get_info(config, types, 'cls_id', 'cls_name')
        download(url, path)

        if types == 'Acne':
            url, path = get_info(config, types, 'embedding_id', 'embedding_name')
            download(url, path)