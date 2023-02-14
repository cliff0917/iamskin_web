
import torch
import torchvision

createClass = lambda name: type(name, (), {'getDictionary':lambda self: dict(vars(self))})

class Model(torch.nn.Module):

    
    def __init__(self, device='cuda'):
        
        super(Model, self).__init__()
        pass
        layer = {}
        layer['0'] = torch.nn.Sequential(
            torch.nn.Linear(2048+27, 1024), 
            torch.nn.BatchNorm1d(1024),
            torch.nn.ReLU(),
            torch.nn.Linear(1024, 512), 
            torch.nn.BatchNorm1d(512),
            torch.nn.ReLU(),
            torch.nn.Linear(512, 256), 
            torch.nn.BatchNorm1d(256),
            torch.nn.ReLU(), 
            torch.nn.Linear(256, 2)
        )
        layer = torch.nn.ModuleDict(layer).to(device)
        pass

        self.device = device
        self.layer = layer
        return

    def getScore(self, batch):

        Neuron = createClass(name='Neuron')
        pass

        layer = self.layer
        neuron = Neuron()
        pass

        neuron.c0 = torch.cat([batch.extraction, batch.encoding], dim=1)
        neuron.c1 = layer['0'](neuron.c0)
        pass

        score = neuron.c1
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


