
import torch
import torchvision

createClass = lambda name: type(name, (), {})

class Encoder(torch.nn.Module):

    def __init__(self, device='cpu'):

        super(Encoder, self).__init__()
        layer = {
            '0' : torch.nn.Sequential(
                torch.nn.Linear(2048, 1024),
                torch.nn.BatchNorm1d(1024),
                torch.nn.LeakyReLU(),
                torch.nn.Linear(1024, 512),
                torch.nn.BatchNorm1d(512),
                torch.nn.LeakyReLU(),
                torch.nn.Linear(512, 256),
                torch.nn.BatchNorm1d(256),
                torch.nn.LeakyReLU(),
                # torch.nn.Linear(256, 8),
                torch.nn.Linear(256, 27),
                torch.nn.Sigmoid(),
            ),
            # '1' : torch.nn.Linear(8, 128),
            # '2' : torch.nn.Linear(8, 128)
            '1' : torch.nn.Linear(27, 128),
            '2' : torch.nn.Linear(27, 128)
        }
        self.layer = torch.nn.ModuleDict(layer)
        self.device = device
        pass

    def getEncoding(self, batch):

        Neuron = createClass(name='Neuron')
        pass

        # print(self.device)
        layer = self.layer#.to(self.device)
        neuron = Neuron()
        pass

        neuron.c0 = batch.extraction
        # print(neuron.c0)
        # print(self.device)
        neuron.c1 = layer['0'](neuron.c0)
        pass

        encoding = neuron.c1
        return(encoding)

    def getEstimation(self, batch):

        Neuron = createClass(name='Neuron')
        pass

        layer = self.layer.to(self.device)
        neuron = Neuron()
        pass

        encoding = self.getEncoding(batch)
        neuron.c0 = encoding
        neuron.c1 = layer['1'](neuron.c0)
        neuron.c2 = layer['2'](neuron.c0)
        pass

        mu, sigma = neuron.c1, neuron.c2
        estimation = (mu, sigma)
        return(estimation)

    def forwardProcedure(self, batch):

        encoding = self.getEncoding(batch)
        estimation = self.getEstimation(batch)
        pass

        procedure = encoding, estimation
        return(procedure)

    pass

##
class Decoder(torch.nn.Module):

    def __init__(self, device):

        super(Decoder, self).__init__()
        layer = {
            "0" : torch.nn.Sequential(
                torch.nn.Linear(128, 256),
                torch.nn.Linear(256, 512),
                torch.nn.BatchNorm1d(512),
                torch.nn.LeakyReLU(),
                torch.nn.Linear(512, 1024),
                torch.nn.BatchNorm1d(1024),
                torch.nn.LeakyReLU(),
                torch.nn.Linear(1024, 2048)
            )
        }
        self.layer = torch.nn.ModuleDict(layer)
        self.device = device
        return

    def getDecoding(self, batch):

        Neuron = createClass(name='Neuron')
        pass

        layer = self.layer.to(self.device)
        neuron = Neuron()
        pass
        
        code = getattr(batch, 'code', None)
        assert code!=None, '[code] is None'
        pass

        neuron.c0 = code
        neuron.c1 = layer['0'](neuron.c0)
        pass

        decoding = neuron.c1
        return(decoding)

    def forwardProcedure(self, batch):

        decoding = self.getDecoding(batch)
        return(decoding)

    pass

class Model(torch.nn.Module):

    def __init__(self, device='cpu'):

        super(Model, self).__init__()
        self.encoder = Encoder(device=device)
        self.decoder = Decoder(device=device)
        self.device  = device
        return

    """
    Reparameterization trick to sample from N(mu, var) from N(0,1).
    :param mu: (Tensor) Mean of the latent Gaussian [B x D]
    :param logvar: (Tensor) Standard deviation of the latent Gaussian [B x D]
    :return: (Tensor) [B x D]
    """
    def runReparameterization(self, estimation):

        # std = torch.exp(0.5 * value['sigma'])
        mu, sigma = estimation
        deviation = torch.exp(sigma)  ##  std
        epsilon = torch.randn_like(deviation)
        pass

        mu        = mu.to(self.device)
        sigma     = sigma.to(self.device)
        deviation = deviation.to(self.device)
        epsilon   = epsilon.to(self.device)
        pass

        parameter = epsilon * deviation + mu
        return(parameter)

    def getEncoding(self, batch):

        encoding = self.encoder.getEncoding(batch)
        return(encoding)

    def forwardProcedure(self, batch):

        encoding = self.getEncoding(batch)
        pass

        mu, sigma = self.encoder.getEstimation(batch)
        estimation = (mu, sigma)
        parameter  = self.runReparameterization(estimation)
        pass

        batch.code = parameter
        decoding   = self.decoder.getDecoding(batch)

        return(encoding, decoding, estimation)
        # mu, log_var = self.encode(input)
        # value = {
        #     "image":None,
        #     "mu":None,
        #     "log(sigma^2)":None,
        #     'reconstruction':None            
        # }
        # value = {}
        # value['feature'] = batch.extraction
        # value['encode_feature'], value['mu'], value['sigma'] = self.encoder(batch)
        # batch.encode_feature = value['encode_feature']
        # # mu, log_var = self.encoder_layer(x)
        # z = self.reparameterize(value)
        # value['reconstruction'] = self.decoder(batch)
        # # return  [self.decode(z), input, mu, log_var]
        # return(value)

    def getCost(self, batch):

        Cost     = createClass(name='Cost')
        Criteria = createClass(name='Criteria')
        cost     = Cost()
        criteria = Criteria()
        pass

        criteria.reconstruction = torch.nn.MSELoss()
        criteria.projection = torch.nn.L1Loss()
        pass

        encoding, decoding, estimation = self.forwardProcedure(batch)
        mu, sigma = estimation
        pass

        divergence = - 0.5 * torch.sum(1 + sigma - (mu ** 2) - sigma.exp(), dim=1)
        reconstruction = criteria.reconstruction(decoding, batch.extraction)
        cost.projection = criteria.projection(encoding, batch.attribution)
        cost.divergence = torch.mean(divergence, dim=0)
        cost.reconstruction = reconstruction
        cost.loss = 0.5*cost.divergence + 0.5*cost.reconstruction + 2*cost.projection
        pass
        
        
        """
        Computes the VAE loss function.
        KL(N(\mu, \sigma), N(0, 1)) = \log \frac{1}{\sigma} + \frac{\sigma^2 + \mu^2}{2} - \frac{1}{2}
        :param args:
        :param kwargs:
        :return:
        loss = {
            "kl-divergence":None,
            "reconstruction":None,
            "total":None
        }
        weight = {"kl-divergence":1}
        loss['reconstruction'] = functional.mse_loss(value['reconstruction'], value['feature'])
        # divergence = - 0.5 * torch.sum(1 + value['log(sigma^2)'] - value['mu'] ** 2 - value['log(sigma^2)'].exp(), dim = 1) 
        divergence = - 0.5 * torch.sum(1 + value['sigma'] - ( value['mu'] ** 2) - value['sigma'].exp(), dim=1)
        loss['kl-divergence'] = torch.mean(divergence, dim = 0)
        loss['total'] = loss['reconstruction'] + weight['kl-divergence'] * loss['kl-divergence']
        return(loss)
        """
        return(cost)

    # def getCost(self, batch):

    #     cost = createPack(name='cost')
    #     value = self.forward(batch)
    #     cost.loss = self.cost(value)
    #     return(cost)
    # def generate(self, number):

    #     device = "cuda" if next(self.decoder.parameters()).is_cuda else "cpu"
    #     z = torch.randn(number, 128).to(device)
    #     samples = self.decoder(z)
    #     return samples
    #     # return self.forward(input=x)[0]

    pass


'''
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


'''