from google import genai
from google.genai import types
from ai.LocalModels.plant_disease_detector import PlantDiseaseDetectorONNX
from typing import List
import json

class ImageAI:
  def __init__(self):
    self.client = genai.Client()


  def isPlantImage(self,image_bytes):
    image = types.Part.from_bytes(
    data=image_bytes, mime_type="image/jpeg"
  )

    response = self.client.models.generate_content(
      model="gemini-2.5-flash",
      contents=["ans in true or false? Is this image of plant or leaves of plant or anything related to it as I am trying to find the diseases in plants?", image],

      # contents=[my_file, "Is this image of plant as I am trying to find the diseases in plants?"],
      config={
        "response_mime_type": "application/json",
        "response_schema": bool,
    },
    )
    return response.text

  def diseaseSuggestions(self, disease_name: str) -> List[str]:
    try:
        response = self.client.models.generate_content(
            model="gemini-2.5-pro",
            contents=[
                f"You are an agricultural expert. Give 2-3 short, clear, and practical suggestions to cure or manage the disease '{disease_name}' in crops. "
                f"Keep suggestions simple so small and marginal farmers can understand. "
                f"Return only a JSON array of strings, e.g. ['Use organic pesticide', 'Keep soil moist']."
            ],
            config={
                "response_mime_type": "application/json",
                "response_schema":{
                "type": "array",
                "items": {"type": "string"}
            }

            },
        )

        # Gemini kabhi kabhi plain string de deta hai, to safe parse karte hain:
        suggestions = response.text
        if isinstance(suggestions, str):
            try:
                suggestions = json.loads(suggestions)
            except json.JSONDecodeError:
                suggestions = [suggestions]  # fallback

        # Ensure it's a list of strings
        if not isinstance(suggestions, list):
            suggestions = [str(suggestions)]

        return suggestions

    except Exception as e:
        print(f"Error fetching suggestions: {e}")
        return ["Unable to fetch suggestions at the moment."]


  def detectPlantDisease(self,image_bytes):
    detect_disease = PlantDiseaseDetectorONNX()
    return detect_disease.predict(image_bytes)

