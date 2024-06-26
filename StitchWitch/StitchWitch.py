from rxconfig import config
import reflex as rx
# from .videocapture import capture_frames_from_video_async
import asyncio
from .videocapture import *
from .about import about

from pathlib import Path  # Import Path from pathlib module

docs_exist = 0
# warning = 0
# warning_color = "green"

style = {
        "background-color": "#0C0E11",  # Dark background color
        "color": "#FFFFFF",  # White text color for contrast
        "font-family": "sans-serif",  # Default font
        "margin": 0,  # Remove default margin
        "height": "100vh",  # Full viewport height
        # "display": "flex",
        "overflow": "hidden",
    }
color = "#ab8bff"

class State(rx.State):
    """The app state."""
    docs: list[str] = []
    docs_exist=False
    
    current_text = ""
    warning = ""
    danger = False
    danger_detail = ""

    click = False
    project_name = ""
    file_loc = "data/docs/lumbar_discectomy.pdf"
    warning_color = "green"

    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of a PDF file."""
        if files is not None:
            for file in files:
                upload_data = await file.read()
                outfile = Path("data/docs") / file.filename
                # Save the file.
                with outfile.open("wb") as file_object:
                    file_object.write(upload_data)
                # Update the img var.
                self.docs.append(file.filename)
        # Update docs_exist based on the presence of docs
        self.docs_exist = True if self.docs else False

    async def run(self):
        executor = ThreadPoolExecutor(max_workers=1)
        # await asyncio.sleep(1)
        try:
            async for response,click in analyze_video_async(self.project_name,self.file_loc):
                self.current_text=response['caption']
                self.warning=response['warning']
                self.danger=response['danger']
                self.danger_detail=response['danger_detail']
                self.click=click
                # print(self.current_text)
                if self.danger == "true":
                    self.warning_color = "red"
                else:
                    self.warning_color = "green"

                yield
        finally:
            executor.shutdown()
        # print(self.current_text)

def index() -> rx.Component:

    # asyncio.run(analyze_video_async("assets/video/eye_surgery.mp4"))

    return rx.vstack(
        rx.hstack(
            rx.link(rx.image(src="/logo.png", width="260px", height="auto", margin_left="30px", margin_top="23px"),href="../",),
            rx.spacer(),
            rx.link(rx.text("About"),margin_right="50px", margin_top="30px", color="white", 
                _hover={
                            "opacity": 0.7,
                        },
                        box_shadow="rgba(151, 65, 252, 0.8) 0 15px 30px -10px",
                        font_weight="600"
                        ,href="/about",
                        ),
                        width="100%",
        ),
        rx.vstack(
            rx.heading(
                    "This is StitchWitch,",
                    font_size="60px",
                    # background_image= "linear-gradient(95deg, #D6D6ED 42.14%, #727280 63.21%)",
                    style={

                        "color": "transparent",
                        "background-image": "linear-gradient(95deg, #D6D6ED 42.14%, #727280 63.21%)",
                        "background-clip": "text",
                        "-webkit-background-clip": "text",  # For WebKit browsers
                        "-webkit-text-fill-color": "transparent",  # Necessary for webkit browsers
                        "line-height": "1.2",  # Increased line height
                        "padding-top": "20px",  # Add padding at the top
                    },
                    height="auto",
                    
            ),
            rx.heading(
                "the modern AI surgery assistant",
                font_size="60px",
                style={
                        "color": "transparent",
                        "background-image": "linear-gradient(95deg, #D6D6ED 42.14%, #727280 63.21%)",
                        "background-clip": "text",
                        "-webkit-background-clip": "text",  # For WebKit browsers
                        "-webkit-text-fill-color": "transparent",  # Necessary for webkit browsers
                        "line-height": "1.2",  # Increased line height  # Add padding at the top
                        "padding-bottom": "20px",  # Add padding at the bottom
                    },
                margin_top="-18px",
               
            ),
            rx.vstack(
                rx.center(
                    rx.heading("Select the Surgery Type", size="5", margin_bottom="10px", margin_top="-20px"),
                    width="100%",
                ),
                # rx.text(State.project_name),
                rx.center(
                    rx.select(
                        ['lumbar_discectomy', 'heart_transplant', 'cataract_surgery'],
                        placeholder="Surgery Type",
                        label="Surgery Types",
                        align_items="center",
                        on_change=State.set_project_name
                    ),
                    width="100%",
                ),
                #pdf upload
                rx.center(
                    rx.upload(
                        rx.vstack(
                            rx.heading("Drag and drop Medical Procedure here or click to select", size="5", margin_bottom="10px"),
                            rx.cond(
                                State.docs_exist==True,
                                rx.button("✅ Selected", color=color, bg="white", border=f"1.5px solid {color}", font_weight="600"),
                                rx.button("Select PDF", color=color, bg="white", border=f"1.5px solid {color}", font_weight="600"),
                            ),
                            align_items="center",  # Center align items horizontally within the vertical stack
                            justify_content="center",  # Center content vertically within the container, if needed
                        ),
                        id="upload1",
                        multiple=False,
                        accept={"application": ["pdf"]},
                        max_files=1,
                        disabled=False,
                        on_keyboard=True,
                        on_drop=State.handle_upload(rx.upload_files(upload_id="upload1")),
                        border=f"1px solid {color}",
                        padding="2.5em",
                        justify_content="center",
                        margin_top="40px",
                    ),
                    width="100%"
                ),
                rx.center(
                    rx.cond(
                        (State.docs_exist==True) & (State.project_name != ""),
                        rx.link(
                            rx.button(
                                "Submit",
                                type="submit",
                                border_radius="1em",
                                box_shadow="rgba(151, 65, 252, 0.8) 0 15px 30px -10px",
                                background_image="linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)",
                                box_sizing="border-box",
                                color="white",
                                opacity=1,
                                _hover={
                                    "opacity": 0.5,
                                },
                                width="100px"
                            ),
                            href="http://localhost:3000/main",
                        ),
                        rx.button(
                                "Submit",
                                type="submit",
                                border_radius="1em",
                                box_shadow="rgba(151, 65, 252, 0.8) 0 15px 30px -10px",
                                background_image="linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)",
                                box_sizing="border-box",
                                color="white",
                                opacity=1,
                                _hover={
                                    "opacity": 0.5,
                                },
                                width="100px"
                        ),
                    ),
                    width="100%",
                    margin_top="30px"
                ),
                padding="2em",
                width="100%",
            ),
            margin_top="5.5vh",  # Center horizontally
            align_items="center",
            width="100%",
            height="100%", 
        ),
        width="100%"
        
        
    )

@rx.page(on_load=State.run)
def main() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.link(rx.image(src="/logo.png", width="260px", height="auto", margin_left="30px", margin_top="23px"),href="../",),
            rx.spacer(),
            rx.link(rx.button(
                "← Back", margin_right="30px", margin_top="40px", color="white", 
                _hover={
                            "opacity": 0.7,
                        },
                border_radius="1em",
                        box_shadow="rgba(151, 65, 252, 0.8) 0 15px 30px -10px",
                        background_image="linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)",
                        box_sizing="border-box",
                        opacity=1,
                        font_weight="600",
                ),
                href="../",
                ),
                width="100%",
                
        ),

            rx.hstack(
                rx.vstack(
                    rx.hstack(
                        rx.chakra.stack(
                            rx.chakra.skeleton_circle(size="10px",start_color="red",width="20px",),
                            margin_top="17px", margin_left="50px", margin_bottom="15px",
                            height="20px",
                            border_radius="200px",
                        ),
                        rx.heading("Live Procedure",  font_size="30px",margin_top="10px", margin_left="8px", margin_bottom="15px"),
                    ),
                    rx.cond(
                        State.project_name == "lumbar_discectomy",
                        rx.vstack(
                            rx.video(
                            url="../lumbar_discectomy.mp4",
                            height="68.2vh",
                            width="120.6vh",
                            
                            playing=State.click,
                            playbackRate='0.5',
                            muted=True,
                            controls=False,
                        ),
                        height="69.2vh",
                        width="121.6vh",
                        border=f"4px solid {State.warning_color}",
                        margin_left="50px",
                        ),
                        rx.chakra.skeleton()
                    ),
                    rx.cond(
                        State.project_name == "cataract_surgery",
                        rx.vstack(
                            rx.video(
                            url="../cataract_surgery.mp4",
                            height="68.2vh",
                            width="120.6vh",
                            
                            playing=State.click,
                            playbackRate='0.5',
                            muted=True,
                            controls=False,
                        ),
                        height="69.2vh",
                        width="121.6vh",
                        border=f"4px solid {State.warning_color}",
                        margin_left="50px",
                        ),
                        rx.chakra.skeleton()
                    ),
                    rx.cond(
                        State.project_name == "heart_transplant",
                        rx.vstack(
                            rx.video(
                            url="../heart_transplant.mp4",
                            height="68.2vh",
                            width="120.6vh",
                            
                            playing=State.click,
                            playbackRate='0.5',
                            muted=True,
                            controls=False,
                        ),
                        height="69.2vh",
                        width="121.6vh",
                        border=f"4px solid {State.warning_color}",
                        margin_left="50px",
                        ),
                        rx.chakra.skeleton()
                    ),
                    width="100%",
                ),
                rx.spacer(),
                rx.container(
                    rx.vstack(
                        rx.heading("Observation", margin_top="10px", margin_bottom="15px", font_size="30px"),
                        rx.vstack(
                            State.current_text,
                            background_color="#222423",
                            width="57vh",
                            height="30.7vh",
                            padding="1.5em",
                            
                        ),
                        rx.heading("Warnings", margin_top="10px", margin_bottom="15px", font_size="30px"),
                        rx.vstack(
                            State.warning,
                        rx.cond(
                            State.danger == "true",
                            rx.vstack(
                                 State.danger_detail,
                                 margin_top="30px",
                                color="red",
                                # border_update = "4px solid red"
                                warning_color = "red"
                            ),
                            rx.vstack(
                                # State.danger_detail,
                                # border_update = "4px solid green"
                                warning_color = "green"
                                
                            ),
                        ),
                        background_color="#222423",
                            width="57vh",
                            height="40vh",
                            padding="1.5em",
                            color="orange",
                        ),
                        flex="1",
                        margin_right="50px",
                    ),
                ),
                
                width="100%",
            ),
            rx.center(
                rx.cond(
                    State.click,
                    rx.vstack(
                    ),
                    rx.chakra.hstack(
                        rx.chakra.circular_progress(is_indeterminate=True, size="100px", color="#7244ee"),
                    ),
                ),
                width="100%",
                margin_top="-500px",
                margin_left="-300px"
            ),    
    )   
    



app = rx.App(style=style)
app.add_page(index)
app.add_page(main, route="/main")
app.add_page(about)
