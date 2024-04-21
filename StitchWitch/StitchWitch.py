from rxconfig import config
import reflex as rx
import asyncio
from .videocapture import *

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
    current_text = "initial text"

    async def run(self):
        executor = ThreadPoolExecutor(max_workers=1)
        try:
            async for response in analyze_video_async("assets/video/eye_surgery.mp4"):
                self.current_text=response
                # print(self.current_text)
                yield
        finally:
            executor.shutdown()
        # print(self.current_text)

# class CondState(rx.State):
#     show: bool = True

#     async def change(self):
#         asyncio.run(analyze_video_async("assets/video/eye_surgery.mp4"))
#         self.show = not (self.show)


@rx.page(on_load=State.run)
def index() -> rx.Component:

    # asyncio.run(analyze_video_async("assets/video/eye_surgery.mp4"))

    return rx.vstack(
        rx.hstack(
            rx.image(src="/logo.png", width="260px", height="auto", margin_left="30px", margin_top="23px"),
        ),
        rx.hstack(
            rx.vstack(
                rx.heading("Live Procedure", margin_top="10px", margin_left="30px", margin_bottom="15px", font_size="30px"),
                # rx.cond(
                #     CondState.show,
                #     rx.button("Toggle", on_click=CondState.change),
                #     rx.video(
                #     url="sample-video.mp4",
                #     height="63vh",
                #     width="112vh",
                #     margin_left="30px",
                #     border="3px solid green",
                #     ),
                # ),
                rx.video(
                    url="sample-video.mp4",
                    height="63vh",
                    width="112vh",
                    margin_left="30px",
                    border="3px solid green",
                    playing=True,
                    ),
            ),
            rx.vstack(
                rx.heading("Caption",margin_left="15px", margin_top="10px", margin_bottom="15px", font_size="30px"),
                rx.vstack(
                    State.current_text,
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
    )

app = rx.App(style=style)
app.add_page(index)
