from rxconfig import config
import reflex as rx


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
        height="100vh",
    )

app = rx.App()
app.add_page(index)
