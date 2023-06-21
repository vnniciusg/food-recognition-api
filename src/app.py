import torch
import torch.nn as nn
from torchvision import models, transforms
from flask import Flask, request, jsonify
from PIL import Image

app = Flask(__name__)

preprocess = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
    ]
)

# Carregar classes
with open("src/classes.txt", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Carregar modelo
model = models.resnet18(pretrained=False)
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, len(classes))
model.load_state_dict(torch.load("src/modelo.pth"))
model.eval()


@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo encontrado"})

    file = request.files["file"]

    try:
        image = Image.open(file)
        image = image.convert("RGB")
        image = preprocess(image)
        image = image.unsqueeze(image, 0)

        with torch.no_grad():
            outputs = model(image)
            _, predicted = torch.max(outputs, 1)
            class_index = predicted.item()
            class_name = classes[class_index]

        return jsonify({"class_index": class_index, "class_name": class_name})

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(port=5003)
