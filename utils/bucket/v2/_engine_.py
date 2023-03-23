
import functools
import pandas
import torch
import os
import PIL.Image
import torchvision.transforms
import PIL.Image
import pickle

createClass = lambda name: type(name, (), {})

def loadPickle(path):

    with open(path, 'rb') as paper:

        content = pickle.load(paper)
        pass

    return(content)

class Set(torch.utils.data.Dataset):

    def __init__(self, configuration, title):
        
        self.configuration = configuration
        self.title = title
        return

    def __getitem__(self, index):

        item = {}
        for key, value in self.dictionary.items():

            if(key=='image'):      item[key] = value[index]
            if(key=='prediction'): item[key] = value[index]
            if(key=='extraction'): item[key] = value[index,:]
            if(key=='target'):     item['label'] = value[index]
            continue
        
        row = self.table['target']==item['label']
        column = ~self.table.columns.isin(['target'])
        item['attribution'] = self.table.loc[row, column]
        pass

        item = item
        return(item)
    
    def __len__(self):

        key    = 'size'
        length = sum(self.dictionary[key])
        return(length)

    def LoadData(self):
        
        path = self.configuration[self.title]['dictionary']
        dictionary = loadPickle(path)
        pass

        path = self.configuration['attribution']['table']
        table = pandas.read_csv(path)
        pass

        self.dictionary = dictionary
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
    pass

    batch.image       = []
    batch.label      = []
    batch.prediction  = []
    batch.extraction  = []
    batch.attribution = []
    for number, item in enumerate(iteration):
        
        image = item['image']
        pass

        label = item['label']
        pass

        prediction = item['prediction']
        pass

        extraction = torch.tensor(item['extraction']).unsqueeze(0).type(torch.FloatTensor)
        pass

        attribution = torch.tensor(item['attribution'].values).type(torch.FloatTensor)
        pass

        batch.image       += [image]
        batch.label       += [label]
        batch.prediction  += [prediction]
        batch.extraction  += [extraction]
        batch.attribution += [attribution]
        continue
    
    batch.configuration = configuration
    batch.inference     = inference
    batch.size          = number + 1
    batch.iteration     = iteration
    batch.device        = device
    batch.extraction  = torch.cat(batch.extraction, axis=0).to(device)
    batch.attribution = torch.cat(batch.attribution, axis=0).to(device)
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

