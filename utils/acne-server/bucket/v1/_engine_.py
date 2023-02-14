
import functools
import pandas
import torch
import os
import PIL.Image
import torchvision.transforms
import PIL.Image

createClass = lambda name: type(name, (), {})

class Set(torch.utils.data.Dataset):

    def __init__(self, configuration, title):
        
        self.configuration = configuration
        self.title = title
        return

    def __getitem__(self, index):

        item = self.table.loc[index]
        return(item)
    
    def __len__(self):

        length = len(self.table)
        return(length)

    def LoadData(self):

        ##  Table
        path = self.configuration[self.title]['table']
        table = pandas.read_csv(path)
        self.table = table
        return

    pass    

def createLoader(set=None, batch=32, inference=False, device='cpu'):

    configuration = set.configuration
    pass

    loader = torch.utils.data.DataLoader(
        dataset=set, batch_size=batch, 
        shuffle=False if(inference) else True, 
        drop_last=False if(inference) else True, 
        collate_fn=functools.partial(collectBatch, configuration=configuration, inference=inference, device=device)
        )
    return(loader)

def getSample(loader):

    batch = next(iter(loader))
    return(batch)

def collectBatch(iteration=None, configuration=None, inference=False, device='cpu'):

    Batch = createClass(name='Batch')
    batch = Batch()
    # pass

    batch.image       = []
    batch.picture     = []
    batch.feature     = []
    batch.target      = []
    for number, item in enumerate(iteration):
        
        image = item['image_name']
        pass

        picture = loadPicture(configuration['image'], image)
        picture = transformPicture(picture, inference)
        picture = picture.unsqueeze(0)
        pass

        # target = configuration['label'].get(item['label'])
        target = item['label']
        target = torch.tensor(target)
        target = target.type(torch.LongTensor)
        target = target.unsqueeze(0)
        pass

        batch.image   += [image]
        batch.picture += [picture]
        batch.target  += [target]
        continue

    batch.iteration = iteration
    batch.inference = inference
    batch.device    = device
    batch.size      = number + 1
    batch.image     = batch.image
    pass

    batch.picture = torch.cat(batch.picture, axis=0).to(device)
    batch.target = torch.cat(batch.target, axis=0).to(device)
    # batch.attribution = torch.cat(batch.attribution, axis=0).to(device)
    return(batch)

def loadPicture(folder, name):

    path = os.path.join(folder, name)
    picture = PIL.Image.open(path).convert("RGB")
    return(picture)

def transformPicture(picture=None, inference=False):

    mu  = [0.46, 0.36, 0.29]
    std = [0.27, 0.21, 0.18]
    layout = (240, 240)
    size = (224, 224)
    pass

    if(inference):

        transform = torchvision.transforms.Compose([
            torchvision.transforms.Resize(layout),
            torchvision.transforms.CenterCrop(size),
            torchvision.transforms.ToTensor(),
            torchvision.transforms.Normalize(mu, std),
        ])
        picture = transform(picture).type(torch.FloatTensor)
        pass

    else:

        transform = torchvision.transforms.Compose([
            torchvision.transforms.Resize(layout),
            torchvision.transforms.RandomCrop(size),
            torchvision.transforms.ToTensor(),
            torchvision.transforms.Normalize(mu, std),
        ])
        picture = transform(picture).type(torch.FloatTensor)
        pass

    return(picture)

