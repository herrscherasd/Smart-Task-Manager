import google.generativeai as genai

from app.core.config import settings

genai.configure(api_key=settings.gemini_api_key)

model = genai.GenerativeModel(settings.gemini_model)