
import pprint
# import numpy
import torch
import types
import PIL.Image
import torchvision

code = {
    'partition':{
        "鼻子區域": 0,
        "額頭區域": 1,
        "臉頰區域": 2,
        "嘴巴、下巴區域": 3,
        "我不確定": 4
    },
    'howlong':{
        "三個月以下": 0,
        "三個月以上": 1     
    },
    'squeeze':{
        "沒有": 0,
        "有": 1,
        
    },
    'cream':{
        "沒有": 0,    
        "有，非藥用抗痘產品": 1,
        "有，藥局購買的外用藥": 2,
        "有，醫師開立的外用藥": 3,
    },
    'medicine':{
        "否": 0,
        "是": 1
    },
    'age':{
        "18歲以下": 0,
        "19-25歲": 1,
        "26-40歲": 2,
        "41-50歲": 3,
        "51歲以上": 4,
    },
    'sex': {
        "女性": 0,
        "男性": 1,
        "不想回答": 2
    },
    'menstruation': {
        "否": 0,
        "是": 1,
        "我不確定": 2,
        "性別男性跳過": 3
    }
}

class Interface:

    def __init__(self, device='cpu'):
        self.device = device
        return
    
    def loadModel(self, path='path/model.pt'):
        self.model = torch.jit.load(path, map_location=self.device)
        return

    def loadData(self, path='path/picture.jpg'):
        data = types.SimpleNamespace(
            picture = PIL.Image.open(path).convert("RGB")
        )
        self.data = data
        return

    def processData(self):
        inference = True
        argument = types.SimpleNamespace(
            mean      = [0.46, 0.36, 0.29],
            deviation = [0.27, 0.21, 0.18],
            layout    = (240, 240),
            size      = (224, 224)    
        )
        kit = torchvision.transforms
        if(inference):
            transform = kit.Compose([
                kit.Resize(argument.layout),
                kit.CenterCrop(argument.size),
                kit.ToTensor(),
                kit.Normalize(argument.mean, argument.deviation),
            ])
        else:
            transform = kit.Compose([
                kit.Resize(argument.layout),
                kit.RandomCrop(argument.size),
                kit.ToTensor(),
                kit.Normalize(argument.mean, argument.deviation),
            ])
        picture = self.data.picture
        picture = transform(picture).type(torch.FloatTensor)
        picture = picture.unsqueeze(0)
        picture = picture.to(self.device)
        self.data.picture = picture
        return

    def getPrediction(self):
        prediction = []
        self.model.eval()
        score = self.model.forward(self.data.picture)
        for c, s in zip(code, score):
            v = s.squeeze().detach().numpy().tolist()
            question = c
            option = list(code[c].keys())
            value = [round(_, 3) for _ in v]
            item = (question, option, value)
            prediction += [item]
            continue
        # pprint.pprint(prediction)
        prediction = sum([v for _,_,v in prediction], [])
        # print(prediction)
        return(prediction)
    pass




# import torch

# torch.jit.load('./log/model/4-epoch.pt', map_location='cpu')
