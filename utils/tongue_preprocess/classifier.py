import warnings

warnings.filterwarnings('ignore')

import cv2, torch
import numpy as np
import torchvision
from torchvision import transforms
from torchvision.transforms import ToTensor

from network.tongue_classifier import CnnModel

def predict(model, classes, img):
    img = process(img)
    xb = img.unsqueeze(0) # Convert to a batch of 1
    yb = model(xb) # Get predictions from model
    _, preds  = torch.max(yb, dim=1)  # Pick index with highest probability
    return classes[preds[0].item()] # Retrieve the class label


# 對 pil_img 進行處理
def process(pil_image):
    img = np.array(pil_image) # 將 PIL img 轉成 cv2 img
    re_img = cv2.resize(img, (32, 32), interpolation=cv2.INTER_AREA)
    transform = transforms.Compose([
        transforms.ToTensor()
    ])
    img_tensor = transform(re_img)
    return img_tensor


def load_model(path):
    model = CnnModel()
    model.load_state_dict(torch.load(path, map_location=torch.device('cpu')))
    return model


if __name__ == '__main__':
    classes = ['black', 'normal', 'white', 'yellow']
    img = cv2.imread("./test.jpg")
    model = load_model('./tongue/classifier/cnn.pth')
    predict_class = predict(model, img, classes)
    print(f'Predicted: {predict_class}')