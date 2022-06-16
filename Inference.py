import torch
import model
import os
import cv2
import albumentations as A
import numpy as np
from albumentations.pytorch import ToTensorV2


class DiseaseClassification:
    def __init__(self, filename):
        self.image = filename
        self.model = model.EfficientNetB0Model()
        self.optimizer = torch.optim.Adam(params = self.model.parameters(), 
                                        lr = 0.0001,
                                        betas = (0.9, 0.999),
                                        eps = 1e-08,
                                        weight_decay = 0.000001,
                                        amsgrad = False)
        self.checkpoint = os.getcwd() + "/Model/DiseaseClassification.pt"
        self.classNameEnglish = ["Healthy", "Leaf Rust", "Powdery Mildew", "Seedling", "Septoria","Stem Rust", "Yellow Rust"]

    def loadCheckpoint(self, model, optimizer):
        checkpoint = torch.load(self.checkpoint, map_location =torch.device('cpu'))
        model.load_state_dict(checkpoint['model'])
        optimizer.load_state_dict(checkpoint['optimizer'])
        return model, optimizer, checkpoint['epoch']
    
    def preprocessImage(self, image, inputImageDim = (512, 512)):
        if image.ndim == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        elif image.ndim == 4:
            image = cv2.cvtColor(image,cv2.COLOR_BGRA2RGB)
    
        ResizedImage = cv2.resize(image, inputImageDim)
        return ResizedImage
    
    def normalizeImage(self, image):
        transform = A.Compose([
            A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
            ToTensorV2()
        ])
        Transformed = transform(image = image)
        TransformedImage = Transformed["image"]
        return TransformedImage

    def prediction(self):
        
        #Load Model
        TrainedModel,_,_ = self.loadCheckpoint(self.model, self.optimizer)
        TrainedModel.eval()

        # Initializing Lists object
        English = []


        with torch.inference_mode():
            
            # Load Image
            image = cv2.imread(self.image)
    
            # Preprocessing Image
            image = self.preprocessImage(image = image)
            
            #Normalize Image
            image = self.normalizeImage(image)
    
            # Permut [channel, width, height]
            #image = torch.permute(image, dims = (2,0,1))
    
            # Unsqueezing Image [batch_size, channel, width, height]
            image = torch.unsqueeze(image, dim = 0)
    
            result = TrainedModel(image)
            #output probabilities
            outputProb = torch.sigmoid(result)
            outputProb = outputProb[0].cpu().detach().numpy()
            #Top Prediction
            PredictedLabels = np.argsort(outputProb)
            for i in range(7):
                englishTup = (self.classNameEnglish[PredictedLabels[i]], outputProb[PredictedLabels[i]])
                English.append(englishTup)
                # print("{}".format(self.classNameEnglish[PredictedLabels[i]]) + "(Confidence = {:.3})".format(outputProb[PredictedLabels[i]]))
                # print("{}".format(self.classNameHindi[PredictedLabels[i]]) + "(आत्मविश्वास = {:.3})".format(outputProb[PredictedLabels[i]]))
                # print("{}".format(self.classNamePunjabi[PredictedLabels[i]] )+"(ਦਾ ਭਰੋਸਾ = {:.3})".format(outputProb[PredictedLabels[i]]))
                # print("*"*20)
        return English
        

if __name__ == "__main__":
    imagePath = os.getcwd() + "/Data" + "/wfd_dataset" + "/40c08000e0f8fdfe.jpg"
    DC = DiseaseClassification(filename = imagePath)
    English, Hindi, Punjabi = DC.prediction()







