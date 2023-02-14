
import os
import torch
import tqdm
import numpy
import pprint
import sys
import sklearn.metrics

createClass = lambda name: type(name, (), {'getDictionary':lambda self: dict(vars(self))})
getAverageWeightedSum = lambda number, score, weight: sum([s * w for s, w in zip(score, weight)]) / number

class Machine:

    def __init__(self, model=None):

        self.model  = model
        return

    def loadWeight(self, path, device='cuda'):

        self.model.load_state_dict(torch.load(path, map_location=device))
        # self.model = torch.load(path, map_location=device)
        return

    def loadModel(self, path, device='cuda'):

        self.model = torch.load(path, map_location=device)
        return

    def defineOptimization(self, method='adam'):

        if(method=='adam'):

            self.gradient = torch.optim.Adam(
                self.model.parameters(), 
                lr=0.00001, betas=(0.9, 0.999), eps=1e-08, weight_decay=0, 
                amsgrad=False
            )
            pass

        if(method=='sgd'):

            self.gradient = torch.optim.SGD(
                self.model.parameters(), 
                lr=0.1, momentum=0, dampening=0,
                 weight_decay=0, nesterov=False
            )
            pass

        self.schedule = torch.optim.lr_scheduler.StepLR(self.gradient, step_size=10, gamma=0.1)
        return

    def learnIteration(self, loader=None):
    
        Iteration = createClass(name='Iteration')
        iteration = Iteration()
        iteration.cost  = []
        iteration.size  = []
        pass

        self.model.train()
        progress = tqdm.tqdm(loader, leave=False)
        for batch in progress:

            self.gradient.zero_grad()
            cost = self.model.getCost(batch)
            cost.loss.backward()
            self.gradient.step()
            pass

            description = "loss : {:.2f}".format(cost.loss.item())
            progress.set_description(description)
            pass

            iteration.cost  += [cost]
            iteration.size  += [batch.size]
            continue
        
        self.schedule.step()    
        return

    @torch.no_grad()
    def evaluateIteration(self, loader=None, title=None):

        Iteration = createClass(name='Iteration')
        iteration = Iteration()
        iteration.image      = []
        iteration.size       = []
        iteration.score      = []
        iteration.prediction = []
        iteration.target     = []
        iteration.cost       = []
        pass

        self.model.eval()
        progress = tqdm.tqdm(loader, leave=False)
        for batch in progress:

            score      = self.model.getScore(batch)
            cost       = self.model.getCost(batch)
            pass

            iteration.cost       += [cost]
            iteration.image      += [batch.image]
            iteration.size       += [batch.size]
            iteration.target     += [batch.target.cpu().numpy()]
            iteration.score      += [score.cpu().numpy()]
            iteration.prediction += [score.cpu().numpy().argmax(1)]
            continue
        
        iteration.image = sum(iteration.image, [])
        pass

        Feedback = createClass(name='Feedback')
        feedback = Feedback()
        feedback.size       = iteration.size
        feedback.image      = iteration.image
        feedback.score      = numpy.concatenate(iteration.score, axis=0)
        feedback.prediction = numpy.concatenate(iteration.prediction, axis=-1)
        feedback.target     = numpy.concatenate(iteration.target, axis=-1)
        pass
        
        loss = [c.loss.item() for c in iteration.cost]
        feedback.cost = {
            "loss": getAverageWeightedSum(sum(iteration.size), loss, iteration.size)
        }        
        return(feedback)

    def saveWeight(self, path):

        folder = os.path.dirname(path)
        os.makedirs(folder, exist_ok=True)
        torch.save(self.model.state_dict(), path)

        return

    def saveModel(self, path):

        folder = os.path.dirname(path)
        os.makedirs(folder, exist_ok=True)
        torch.save(self.model, path)

        return

    pass

