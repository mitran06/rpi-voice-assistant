import os, google.generativeai as genai
from config.settings import settings
# from dotenv import load_dotenv  # Remove if not needed

# load_dotenv()  # Remove if .env is loaded in app.py

if os.getenv("GOOGLE_API_KEY") is None:
    raise ValueError("GOOGLE_API_KEY is not set.")
else:
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel(
    "gemini-2.0-flash",
    generation_config={
        "temperature": settings["genai"]["temperature"],
        "max_output_tokens": settings["genai"]["max_output_tokens"],
    },
    system_instruction=settings["genai"]["instruction"],
)

def ask_ai(prompt):
    return model.generate_content(prompt).text
