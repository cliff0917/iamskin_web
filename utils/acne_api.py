
import os
import pprint

from utils import bucket, network, embedding

##  U should load the model in the first, then start infer the case.
api_config = bucket.loadYaml(path='./acne_api.yaml')

def createCase(path):

    import PIL.Image

    Case = bucket.createClass(name='Case')
    case = Case()
    picture = PIL.Image.open(path).convert("RGB")
    picture = bucket.v1.transformPicture(picture=picture, inference=True)
    picture = picture.unsqueeze(0)
    case.picture = picture
    return case


def downloadModels():
    download('image-classifier')
    download('image-embedding')


def download(types):

    import os
    import gdown

    config = api_config[types]
    path = config['path']
    url = config['url']

    if not os.path.exists(path):
        folder = os.path.dirname(path)
        os.makedirs(folder)
        gdown.download(url, path, quiet=False)


def loadModel():

    ##  Image classifier model.
    path = api_config['image-classifier']['path']
    image_classifier = network.v1.Machine(model=None)
    image_classifier.loadModel(path, device='cpu')
    image_classifier.model.eval()

    ##  Image classifier model.
    path = api_config['image-embedding']['path']
    image_embedding = embedding.Interface(device='cpu')
    image_embedding.loadModel(path)
    image_embedding.model.eval()
    return (image_classifier, image_embedding)


def inferCase(case, models, path):

    import torch
    classifier, attr_cls = models

    with torch.no_grad():

        class_score = classifier.model.getScore(batch=case)
        class_prediction = class_score.argmax(1).item()
        class_extraction = classifier.model.getExtraction(batch=case)
        case.extraction = class_extraction

        attr_cls.loadData(path)
        attr_cls.processData()
        class_attribute_prediction = attr_cls.getPrediction()

    return (class_prediction, class_attribute_prediction)