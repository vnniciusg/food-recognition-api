import torch
from torchvision import models
from services.formatImage import convertImage

classes = ["Maça", "Banana"]
num_classes = len(classes)

model_path = "src/model/model.pth"


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def analisyImage(image):
    model = models.resnet50()
    in_features = model.fc.in_features
    model.fc = torch.nn.Linear(in_features, 3)
    model.load_state_dict(torch.load(model_path))
    print("Modelo carregado")

    model.to(device)
    model.eval()

    formatImage = convertImage(image)

    with torch.no_grad():
        output = model(formatImage)
        _, predicted = torch.max(output, 1)
        class_index = predicted.item()

        predicted_class = classes[class_index]

    return predicted_class.lower()
