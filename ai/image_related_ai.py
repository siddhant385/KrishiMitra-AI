from google import genai
from google.genai import types



class ImageAI:
  def __init__(self):
    self.client = genai.Client()


  def isPlantImage(self,image_bytes):
    image = types.Part.from_bytes(
    data=image_bytes, mime_type="image/jpeg"
  )

    response = self.client.models.generate_content(
      model="gemini-2.5-flash",
      contents=["ans in true or false? Is this image of plant as I am trying to find the diseases in plants?", image],

      # contents=[my_file, "Is this image of plant as I am trying to find the diseases in plants?"],
      config={
        "response_mime_type": "application/json",
        "response_schema": bool,
    },
    )
    return response.text
