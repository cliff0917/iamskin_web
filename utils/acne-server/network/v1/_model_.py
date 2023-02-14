
import torch
import torchvision

createClass = lambda name: type(name, (), {})

class Model(torch.nn.Module):

    
    def __init__(self, backbone='resnet', classification=2, device='cuda'):
        
        super(Model, self).__init__()
        pass

        if(backbone=='resnet'):

            giant = torchvision.models.resnet152(weights='ResNet152_Weights.IMAGENET1K_V1')
            net = [i for i in giant.children()][:-1]
            # net = [i for i in torchvision.models.resnet152(pretrained=True).children()][:-1]
            layer = {
                "0":torch.nn.Sequential(*net),
                '1':torch.nn.Sequential(
                    torch.nn.Linear(2048, classification)
                )
            }
            pass
        
        layer = torch.nn.ModuleDict(layer).to(device)
        pass

        self.device = device
        self.classification = classification
        self.backbone = backbone
        self.layer = layer
        return

    def getExtraction(self, batch):

        Neuron = createClass(name='Neuron')
        pass

        backbone = self.backbone
        layer = self.layer
        neuron = Neuron()
        pass

        if(backbone=='resnet'):

            neuron.c0 = batch.picture
            neuron.c1 = layer['0'](neuron.c0).flatten(1, -1)
            extraction = neuron.c1
            pass
        
        return(extraction)

    def getScore(self, batch):

        Neuron = createClass(name='Neuron')
        pass

        backbone = self.backbone
        layer = self.layer
        neuron = Neuron()
        pass

        if(backbone=='resnet'):
    
            neuron.c1 = self.getExtraction(batch)
            neuron.c2 = layer['1'](neuron.c1)
            score = neuron.c2
            pass

        return(score)

    def getCost(self, batch):

        Cost     = createClass('Cost')
        Criteria = createClass('Criteria')
        cost     = Cost()
        criteria = Criteria()
        pass

        target, score = batch.target, self.getScore(batch)
        pass

        # weight = torch.tensor([1.04, 0.83, 2.08, 2.42]).cuda()
        weight = None       
        criteria.cel  = torch.nn.CrossEntropyLoss(weight)
        cost.cel = criteria.cel(score, target)
        pass
        
        cost.loss = cost.cel
        return(cost)

    pass


