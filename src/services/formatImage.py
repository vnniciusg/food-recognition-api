import torch
from torchvision import transforms
from PIL import Image


mean = [0.8316, 0.6671, 0.4760]
std = [0.1642, 0.2702, 0.3001]


transformations = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize((torch.Tensor(mean)), (torch.Tensor(std))),
    ]
)


def convertImage(file):
    image = Image.open(file)
    image = transformations(image)
    image = image.unsqueeze_(0)
    return image
