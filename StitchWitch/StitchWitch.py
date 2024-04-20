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

# # Configure the Gemini API with the loaded API key
# genai.configure(api_key=google_api_key)

# model = genai.GenerativeModel('gemini-pro')
# response = model.generate_content("Give me python code to sort a list")


style = {
        "background-color": "#0C0E11",  # Dark background color
        "color": "#FFFFFF",  # White text color for contrast
        "font-family": "sans-serif",  # Default font
        "margin": 0,  # Remove default margin
        "height": "100vh",  # Full viewport height
        "display": "flex",
    }

class State(rx.State):
    """The app state."""

def index() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.image(src="/logo.png", width="260px", height="auto", margin_left="30px", margin_top="23px"),
        ),
        rx.hstack(
            rx.vstack(
                rx.heading("Live Procedure", margin_top="10px", margin_left="30px", margin_bottom="15px", font_size="30px"),
                rx.vstack(
                    background_color="#222423",
                    height="63vh",
                    width="112vh",
                    margin_left="30px",
                    border="3px solid green", 
                ),
            ),
            rx.vstack(
                rx.heading("Caption",margin_left="15px", margin_top="10px", margin_bottom="15px", font_size="30px"),
                rx.vstack(
                    background_color="#222423",
                    margin_left="15px",
                    width="55vh",
                    height="75vh",
                ),
                flex="1",
            )
        ),
        rx.heading("Warnings: ", margin_top="-90px", margin_left="30px", font_size="20px", color="orange"),
        rx.heading("Dangers: ", margin_left="30px", margin_top="-10px", font_size="20px", color="red"),
        # rx.text(response.text)
    )

app = rx.App(style=style)
app.add_page(index)
