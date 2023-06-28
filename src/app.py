import torch
import torch.nn as nn
from torchvision import models, transforms
from flask import Flask, request, jsonify
from PIL import Image

app = Flask(__name__)

mean = [0.8316, 0.6671, 0.4760]
std = [0.1642, 0.2702, 0.3001]


transformations = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize((torch.Tensor(mean)), (torch.Tensor(std))),
    ]
)

model_path = "src/model.pth"

classes = ["apple", "banana"]
num_classes = len(classes)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo encontrado"})

    file = request.files["file"]

    try:
        image = Image.open(file)
        image = transformations(image)
        image = image.unsqueeze_(0)

        model = models.resnet50()
        in_features = model.fc.in_features
        model.fc = torch.nn.Linear(in_features, 3)
        model.load_state_dict(torch.load(model_path))

        model.to(device)
        model.eval
        with torch.no_grad():
            output = model(image)

            _, predicted = torch.max(output, 1)
            class_index = predicted.item()

            predicted_class = classes[class_index]

            print("Classe prevista: ", predicted_class)

        return jsonify({"Alimento": predicted_class})

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(port=5003, debug=True)
