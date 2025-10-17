from PIL import Image
import torch
import torch.nn as nn
from torchvision import transforms, models

trained_model = None
damage_classes = ['Front Breakage', 'Front Crushed', 'Front Normal', 'Rear Breakage', 'Rear Crushed', 'Rear Normal']

#Load the pre-trained ResNet model
class CarClassifierResNet(nn.Module):
    def __init__(self, dropout_rate=0.3, num_classes=6):
        super().__init__()
        self.model = models.resnet50(weights='DEFAULT')

        in_features = self.model.fc.in_features

        # Freezing all the layers
        for param in self.model.parameters():
            param.requires_grad = False

            # Releasing 4th layer and fcc
        for param in self.model.layer4.parameters():
            param.requires_grad = True

        self.model.fc = nn.Sequential(
            nn.Dropout(dropout_rate),
            nn.Linear(in_features, num_classes)
        )

    def forward(self, x):
        return self.model(x)


def predict(image_path):
    image = Image.open(image_path).convert('RGB')
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    image_tensor = transform(image).unsqueeze(0)

    global trained_model
    if trained_model is None:
        trained_model = CarClassifierResNet()
        trained_model.load_state_dict(torch.load("model/car_model.pth",map_location=torch.device('cpu')))
        trained_model.eval()
    with torch.no_grad():
        output = trained_model(image_tensor)
        _,predicted = torch.max(output,1)
        return damage_classes[predicted.item()]



