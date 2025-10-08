import onnxruntime as ort
from PIL import Image
import numpy as np
import io

class PlantDiseaseDetectorONNX:
    def __init__(self, model_path='ai/models/plant_disease_model.onnx'):
        self.disease_classes = [
            'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
            'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
            'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_',
            'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot',
            'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
            'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
            'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight',
            'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy',
            'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot',
            'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot',
            'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot',
            'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy'
        ]

        self.session = ort.InferenceSession(model_path)

    def preprocess(self, img_bytes):
        image = Image.open(io.BytesIO(img_bytes)).resize((256, 256))
        img = np.array(image).astype(np.float32) / 255.0
        img = np.transpose(img, (2, 0, 1))
        img = np.expand_dims(img, axis=0)
        return img

    def predict(self, img_bytes):
        img = self.preprocess(img_bytes)
        outputs = self.session.run(["output"], {"input": img})
        probs = np.exp(outputs[0]) / np.sum(np.exp(outputs[0]))  # softmax
        top_idx = np.argmax(probs)
        confidence = probs[0][top_idx] * 100
        predicted_class = self.disease_classes[top_idx]

        plant_name, disease = predicted_class.split('___')
        disease = disease.replace('_', ' ')

        severity = "High" if confidence > 90 else "Medium" if confidence > 70 else "Low"

        return {
            "plant_name": plant_name,
            "disease": disease,
            "severity": severity,
            "disease_probability": f"{confidence:.2f}%"
        }
