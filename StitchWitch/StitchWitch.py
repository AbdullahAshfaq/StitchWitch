from rxconfig import config
import reflex as rx
import google.generativeai as genai
import json


# Path to the JSON file containing the API key
json_file_path = 'env.json'

# Load the API key from the JSON file
with open(json_file_path, 'r') as file:
    config = json.load(file)
    google_api_key = config['GOOGLE_API_KEY']

# Configure the Gemini API with the loaded API key
genai.configure(api_key=google_api_key)

# Bypassing safety
safe = [
        {
            "category": "HARM_CATEGORY_DANGEROUS",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
    ]

model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("Give me python code to sort a list")


class State(rx.State):
    """The app state."""

def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Hello!!", size="9"),
            align="center",
            spacing="7",
            font_size="2em",
        ),
        rx.text(response.text),
        height="100vh",
    )

app = rx.App()
app.add_page(index)
