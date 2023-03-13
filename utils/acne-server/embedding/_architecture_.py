
import os
import types
import sklearn.metrics
import torch
import torchvision
import copy

class Backbone(torch.nn.Module):

    def __init__(self, weight='MobileNet_V2_Weights.IMAGENET1K_V1'):
        super(Backbone, self).__init__()
        self.weight = weight
        return
    
    def createLayer(self):
        if(self.weight=='MobileNet_V2_Weights.IMAGENET1K_V1'):
            net = torchvision.models.mobilenet_v2(weights=self.weight)
            layer = torch.nn.Sequential(
                *list(net.children())[:-1],
                torch.nn.AvgPool2d((7,7)),
                torch.nn.Flatten(1, -1)
            )
        self.layer = layer
        return(layer)
    
    def getTube(self):
        if(self.weight=='MobileNet_V2_Weights.IMAGENET1K_V1'): tube = 1280
        return(tube)

    pass

class Classifier(torch.nn.Module):

    def __init__(self, entrance):
        super(Classifier, self).__init__()
        self.entrance = entrance
        return
    
    def createLayer(self):
        c1 = torch.nn.Sequential(
            torch.nn.Linear(self.entrance, 64),
            torch.nn.ReLU(),
            torch.nn.Linear(64, 5)
        )
        c2 = torch.nn.Sequential(
            torch.nn.Linear(self.entrance, 64),
            torch.nn.ReLU(),
            torch.nn.Linear(64, 2)
        )        
        c3 = torch.nn.Sequential(
            torch.nn.Linear(self.entrance, 64),
            torch.nn.ReLU(),
            torch.nn.Linear(64, 2)
        )  
        c4 = torch.nn.Sequential(
            torch.nn.Linear(self.entrance, 64),
            torch.nn.ReLU(),
            torch.nn.Linear(64, 4)
        )              
        c5 = torch.nn.Sequential(
            torch.nn.Linear(self.entrance, 64),
            torch.nn.ReLU(),
            torch.nn.Linear(64, 2)
        )
        c6 = torch.nn.Sequential(
            torch.nn.Linear(self.entrance, 64),
            torch.nn.ReLU(),
            torch.nn.Linear(64, 5)
        )
        c7 = torch.nn.Sequential(
            torch.nn.Linear(self.entrance, 64),
            torch.nn.ReLU(),
            torch.nn.Linear(64, 3)
        )
        c8 = torch.nn.Sequential(
            torch.nn.Linear(self.entrance, 64),
            torch.nn.ReLU(),
            torch.nn.Linear(64, 4)
        )
        self.layer = torch.nn.ModuleList([c1, c2, c3, c4, c5, c6, c7, c8])
        return
    
    pass

class Architecture(torch.nn.Module):

    def __init__(self, device='cuda'):
        super(Architecture, self).__init__()
        ##  Define the backbone.
        backbone = Backbone(weight='MobileNet_V2_Weights.IMAGENET1K_V1')
        backbone.createLayer()
        tube = backbone.getTube()
        classifier = Classifier(entrance=tube)
        classifier.createLayer()
        layer = torch.nn.ModuleDict({
            "backbone": backbone.layer,
            "classifier": classifier.layer
        })
        self.layer = layer.to(device)
        self.device = device
        return

    def getScore(self, batch):
        x = batch.picture
        h = self.layer['backbone'](x)
        y = [
            self.layer['classifier'][0](h),
            self.layer['classifier'][1](h),
            self.layer['classifier'][2](h),
            self.layer['classifier'][3](h),
            self.layer['classifier'][4](h),
            self.layer['classifier'][5](h),
            self.layer['classifier'][6](h),
            self.layer['classifier'][7](h)
        ]
        score = y
        return(score)

    def getCost(self, batch):
        score = self.getScore(batch)
        target = [t.flatten(0, -1) for t in torch.split(batch.target, 1, dim=1)]
        ##  Compute loss.
        weight = None   
        criteria = torch.nn.CrossEntropyLoss(weight)
        individual = [criteria(s, t) for s, t in zip(score, target)]
        total = sum(individual)
        ##  Return cost.
        cost = types.SimpleNamespace(individual=individual, total=total)
        return(cost)

    def getMetric(self, batch):
        self.eval()
        target = [t.flatten(0, -1) for t in torch.split(batch.target, 1, dim=1)]
        score = self.getScore(batch)
        prediction = [torch.argmax(s, dim=1) for s in score]
        measure = [Measure(target=t.to('cpu'), prediction=p.to('cpu')) for t, p in zip(target, prediction)]
        metric = types.SimpleNamespace(
            accuracy=[m.getAccuracy() for m in measure]
        )
        return(metric)

    def forward(self, x):
        h = self.layer['backbone'](x)
        y = [
            self.layer['classifier'][0](h),
            self.layer['classifier'][1](h),
            self.layer['classifier'][2](h),
            self.layer['classifier'][3](h),
            self.layer['classifier'][4](h),
            self.layer['classifier'][5](h),
            self.layer['classifier'][6](h),
            self.layer['classifier'][7](h)
        ]
        y = tuple(y)
        return(y)
    
    pass

class Module:

    def __init__(self, model):
        # checkpoint = './cache'
        # torch.save(model.state_dict(), checkpoint)
        # model.load_state_dict(torch.load(checkpoint))
        # self.model = model
        self.model = copy.deepcopy(model)
        return
    
    def createScript(self, method='forward', shape=(1,3,224,224)):
        device = 'cpu'
        self.model = self.model.to(device)
        sample = torch.randn(shape).to(device)
        self.script = torch.jit.trace_module(self.model, {method : sample})
        return

    def saveScript(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.script.save(path)
        return

    pass
class Measure:

    def __init__(self, target, prediction):
        self.target = target
        self.prediction = prediction
        return
    
    def getAccuracy(self):
        accuracy = sklearn.metrics.accuracy_score(self.target, self.prediction)
        return(accuracy)
    
    pass
