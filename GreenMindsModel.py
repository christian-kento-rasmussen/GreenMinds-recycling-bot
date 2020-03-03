# imports related to PyTorch
import torch
from torch import nn, optim
import torch.nn.functional as F
from torchvision import datasets, transforms, models
from collections import OrderedDict

# python tools
import numpy as np
import pandas as pd
from PIL import Image


class GreenMindsModel:
    def __init__(self, model_path):
        self.model_path = model_path
        self.load_model(self.model_path)

    def load_model(self, model_path):
        '''
            loads a preetrained model of type densenet121
        '''
        # loads the data
        checkpoint = torch.load(model_path, map_location=lambda storage, loc: storage)

        # downloads the pre trained model
        self.model = models.densenet121(pretrained=True)
        for param in self.model.parameters():
            param.requires_gradu = False

        # re-creates the classifier
        prediction_size = len(checkpoint['class_to_idx'])
        classifier = nn.Sequential(OrderedDict([
            ('fc_1', nn.Linear(1024, 512)),
            ('relu_1', nn.ReLU()),
            ('dropout_1', nn.Dropout(.2)),
            ('fc_2', nn.Linear(512, 256)),
            ('relu_2', nn.ReLU()),
            ('dropout_2', nn.Dropout(.2)),
            ('fc_3', nn.Linear(256, prediction_size)),
            ('output', nn.LogSoftmax(dim=1))
        ]))
        self.model.classifier = classifier

        # loads the old weights
        self.model.load_state_dict(checkpoint['model_state_dict'])

        # stores the class_to_idx
        self.model.class_to_idx = checkpoint['class_to_idx']

        # sends the model to the gpu if avaliable
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self.model.to(self.device)

    def process_image(self, image):
        ''' 
            Scales, crops, and normalizes a PIL image for a PyTorch model,
            returns an Numpy array
        '''
        # creates the pre proccessing transforms
        resize = transforms.Compose([
            transforms.Resize(255),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        # applying transforms and returns the image
        return resize(image)

    def predict(self, image, topk=5):
        ''' 
            Predict the class (or classes) of an image using a trained deep learning model.
        '''
        # opens the image and applies preproccessing
        image = self.process_image(image)
        # unsqueezes it
        image = image.unsqueeze_(0)
        # sends it to our device (cpu/gpu)
        image = image.to(self.device)
        self.model = self.model.to(self.device)

        # sets our model to eval mode, to disable dropout
        self.model.eval()
        # stops our optimizer for better performance
        with torch.no_grad():
            # gets our log probabilities from our model
            logps = self.model.forward(image)

        # converts to probabilities
        ps = torch.exp(logps)

        # Get the top 5 probabilities and classes
        prop, classes = ps.topk(topk, dim=1)

        # Get the first items in the tensor list which contains the probs and classes
        top_p = prop.tolist()[0]
        top_classes = classes.tolist()[0]

        # sets up a lost to hold our labels
        labels = []

        # reverses our class_to_idx which our model holds
        idx_to_class = {v: k for k, v in self.model.class_to_idx.items()}

        # loops through each prediction to find the labels instead of numbers
        for c in top_classes:
            # adds the name which our model did predict
            labels.append(idx_to_class[c])

        # returns our top k probabilities and labels as lists.
        return top_p, labels
