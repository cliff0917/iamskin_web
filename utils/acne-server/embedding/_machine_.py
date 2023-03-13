
import types
import torch
import tqdm
import torch.utils.tensorboard

class Machine:

  def __init__(self, model=None, device="cpu"):
      self.model  = model
      self.device = device
      return

  def loadWeight(self, path=None):
      weight = torch.load(path, map_location=self.device)
      self.model.load_state_dict(weight)
      return
 
  def createOptimization(self, method='adam', rate=0.001):
      if(method=='adam'):
          self.gradient = torch.optim.Adam(
              self.model.parameters(), 
              lr=rate, betas=(0.9, 0.999), eps=1e-08, weight_decay=0, 
              amsgrad=False
          )
          pass
      if(method=='sgd'):
          self.gradient = torch.optim.SGD(
              self.model.parameters(), 
              lr=rate, momentum=0, dampening=0,
              weight_decay=0, nesterov=False
          )
          pass
      self.schedule = torch.optim.lr_scheduler.StepLR(self.gradient, step_size=10, gamma=0.1)
      return

  def createIteration(self):
      self.iteration = types.SimpleNamespace(
          learning=0,
          inference=0
      )
      return

  def createWriter(self, folder='./log'):
      self.writer = torch.utils.tensorboard.SummaryWriter(log_dir=folder)
      return
  
  def learnLoader(self, loader=None):
      self.model.train()
      progress = tqdm.tqdm(loader, leave=False)
      for batch in progress:
          self.iteration.learning += 1
          self.gradient.zero_grad()
          cost = self.model.getCost(batch)
          cost.total.backward()
          self.gradient.step()
          pass
          self.writer.add_scalar('train loss (total)', cost.total, self.iteration.learning)
          self.writer.add_scalar('train loss (0)', cost.individual[0], self.iteration.learning)
          self.writer.add_scalar('train loss (1)', cost.individual[1], self.iteration.learning)
          self.writer.add_scalar('train loss (2)', cost.individual[2], self.iteration.learning)
          self.writer.add_scalar('train loss (3)', cost.individual[3], self.iteration.learning)
          self.writer.add_scalar('train loss (4)', cost.individual[4], self.iteration.learning)
          self.writer.add_scalar('train loss (5)', cost.individual[5], self.iteration.learning)
          self.writer.add_scalar('train loss (6)', cost.individual[6], self.iteration.learning)
          self.writer.add_scalar('train loss (7)', cost.individual[7], self.iteration.learning)
          pass
          metric = self.model.getMetric(batch)
          self.writer.add_scalar('train accuracy (0)', metric.accuracy[0], self.iteration.learning)
          self.writer.add_scalar('train accuracy (1)', metric.accuracy[1], self.iteration.learning)
          self.writer.add_scalar('train accuracy (2)', metric.accuracy[2], self.iteration.learning)
          self.writer.add_scalar('train accuracy (3)', metric.accuracy[3], self.iteration.learning)
          self.writer.add_scalar('train accuracy (4)', metric.accuracy[4], self.iteration.learning)
          self.writer.add_scalar('train accuracy (5)', metric.accuracy[5], self.iteration.learning)
          self.writer.add_scalar('train accuracy (6)', metric.accuracy[6], self.iteration.learning)
          self.writer.add_scalar('train accuracy (7)', metric.accuracy[7], self.iteration.learning)
          continue
      self.schedule.step()    
      return

  @torch.no_grad()
  def inferLoader(self, loader=None):
      self.model.eval()
      progress = tqdm.tqdm(loader, leave=False)
      for batch in progress:
        self.iteration.inference += 1
        cost = self.model.getCost(batch)
        pass
        self.writer.add_scalar('test loss (total)', cost.total, self.iteration.inference)
        self.writer.add_scalar('test loss (0)', cost.individual[0], self.iteration.inference)
        self.writer.add_scalar('test loss (1)', cost.individual[1], self.iteration.inference)
        self.writer.add_scalar('test loss (2)', cost.individual[2], self.iteration.inference)
        self.writer.add_scalar('test loss (3)', cost.individual[3], self.iteration.inference)
        self.writer.add_scalar('test loss (4)', cost.individual[4], self.iteration.inference)
        self.writer.add_scalar('test loss (5)', cost.individual[5], self.iteration.inference)
        self.writer.add_scalar('test loss (6)', cost.individual[6], self.iteration.inference)
        self.writer.add_scalar('test loss (7)', cost.individual[7], self.iteration.inference)
        pass
        metric = self.model.getMetric(batch)
        self.writer.add_scalar('test accuracy (0)', metric.accuracy[0], self.iteration.inference)
        self.writer.add_scalar('test accuracy (1)', metric.accuracy[1], self.iteration.inference)
        self.writer.add_scalar('test accuracy (2)', metric.accuracy[2], self.iteration.inference)
        self.writer.add_scalar('test accuracy (3)', metric.accuracy[3], self.iteration.inference)
        self.writer.add_scalar('test accuracy (4)', metric.accuracy[4], self.iteration.inference)
        self.writer.add_scalar('test accuracy (5)', metric.accuracy[5], self.iteration.inference)
        self.writer.add_scalar('test accuracy (6)', metric.accuracy[6], self.iteration.inference)
        self.writer.add_scalar('test accuracy (7)', metric.accuracy[7], self.iteration.inference)
        continue
      return

#   def saveWeight(self, path):
#       folder = os.path.dirname(path)
#       os.makedirs(folder, exist_ok=True)
#       torch.save(self.model.state_dict(), path)
#       return

#   pass


# writer = torch.utils.tensorboard.SummaryWriter(log_dir='./log')
# writer.add_scalar('Loss/train', np.random.random(), epoch)

# from torch.utils.tensorboard import SummaryWriter
# writer = SummaryWriter()
# x = range(100)
# for k in range(5):
#     for i in x:
#         writer.add_scalar('y=2x', i * 2)
# writer.close()