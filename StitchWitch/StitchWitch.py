from rxconfig import config
import reflex as rx


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
        rx.heading("Live Procedure", margin_top="10px", margin_left="30px", margin_bottom="15px", font_size="30px"),
        rx.vstack(
            background_color="#222423",
            height="63vh",
            width="112vh",
            margin_left="30px",
        ),
        rx.heading("Warnings", margin_top="10px", margin_left="30px", font_size="20px", color="orange"),
        rx.heading("Dangers", margin_left="30px", font_size="20px", color="red"),
    )

app = rx.App(style=style)
app.add_page(index)
