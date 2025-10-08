import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import io
from utils.models import ResNet9


class PlantDiseaseDetector:
    def __init__(self, model_path='ai/models/plant_disease_model.pth'):
        # Define all possible classes
        self.disease_classes = [
            'Apple___Apple_scab',
            'Apple___Black_rot',
            'Apple___Cedar_apple_rust',
            'Apple___healthy',
            'Blueberry___healthy',
            'Cherry_(including_sour)___Powdery_mildew',
            'Cherry_(including_sour)___healthy',
            'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
            'Corn_(maize)___Common_rust_',
            'Corn_(maize)___Northern_Leaf_Blight',
            'Corn_(maize)___healthy',
            'Grape___Black_rot',
            'Grape___Esca_(Black_Measles)',
            'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
            'Grape___healthy',
            'Orange___Haunglongbing_(Citrus_greening)',
            'Peach___Bacterial_spot',
            'Peach___healthy',
            'Pepper,_bell___Bacterial_spot',
            'Pepper,_bell___healthy',
            'Potato___Early_blight',
            'Potato___Late_blight',
            'Potato___healthy',
            'Raspberry___healthy',
            'Soybean___healthy',
            'Squash___Powdery_mildew',
            'Strawberry___Leaf_scorch',
            'Strawberry___healthy',
            'Tomato___Bacterial_spot',
            'Tomato___Early_blight',
            'Tomato___Late_blight',
            'Tomato___Leaf_Mold',
            'Tomato___Septoria_leaf_spot',
            'Tomato___Spider_mites Two-spotted_spider_mite',
            'Tomato___Target_Spot',
            'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
            'Tomato___Tomato_mosaic_virus',
            'Tomato___healthy'
        ]

        # Initialize model
        self.model = ResNet9(3, len(self.disease_classes))
        self.model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        self.model.eval()

        # Define transforms
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.ToTensor(),
        ])

    def predict(self, img_bytes):
        """
        Predict disease label, probability, and estimated severity
        :param img_bytes: image in bytes
        :return: dict with plant_name, disease, probability, severity
        """
        image = Image.open(io.BytesIO(img_bytes))
        img_t = self.transform(image)
        img_u = torch.unsqueeze(img_t, 0)

        with torch.no_grad():
            outputs = self.model(img_u)
            probs = F.softmax(outputs, dim=1)
            top_prob, top_idx = torch.max(probs, dim=1)
            confidence = top_prob.item() * 100
            predicted_class = self.disease_classes[top_idx.item()]

        # Parse class into plant and disease
        plant_name, disease = predicted_class.split('___')
        disease = disease.replace('_', ' ')

        # Rough severity estimate
        if confidence > 90:
            severity = "High"
        elif confidence > 70:
            severity = "Medium"
        else:
            severity = "Low"

        return {
            "plant_name": plant_name,
            "disease": disease,
            "severity": severity,
            "disease_probability": f"{confidence:.2f}%"
        }
