import reflex as rx
import cv2
import os
from time import sleep
import asyncio
from PIL import Image 
from pathlib import Path


# Path to the JSON file containing the API key
# json_file_path = 'env.json'

# # Load the API key from the JSON file
# with open(json_file_path, 'r') as file:
#     config = json.load(file)
#     google_api_key = config['GOOGLE_API_KEY']

# Configure the Gemini API with the loaded API key
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
video_path = "sample-video.mp4" # Path to desired video
cap = cv2.VideoCapture(0)
output_folder = "captured_frames"  # Output folder to save captured frames
interval_sec = 1  # Interval in seconds to capture frames
# Get the frame rate of the video
fps = cap.get(cv2.CAP_PROP_FPS)
# Calculate frame interval based on desired interval_sec
frame_interval = int(fps * interval_sec)

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

output_path = Path("assets/frame.jpg")

class State(rx.State):
    """The app state."""
    frame_count = 0
    output_path = "assets/frame.jpg"
    
    async def analyze_video(self):
        while True:
            # Read a frame from the video
            ret, frame = cap.read()
            print("nfaoifnoaenfoenofeao")

            if not ret:
                pass  # Break the loop if we've reached the end of the video

            # Display the current frame (video playback)
            # cv2.imshow("Video Playback", frame)
            output_path = f"assets/frames/frame{self.frame_count}.jpg"
            print(output_path, frame)
            cv2.imwrite(output_path, frame)
            opencv_image = cv2.imread(output_path) 
            frame_rgb = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)
            pil_image.save(output_path)
            
            self.output_path = output_path.removeprefix("assets/")

            # Check if it's time to save a frame
            if self.frame_count % frame_interval == 0:
                # Save the frame as an image file
                output_path = f"{output_folder}/frame_{self.frame_count // frame_interval}.jpg"
                # cv2.imwrite(output_path, frame)
                print(f"Saved frame {self.frame_count // frame_interval}")

            # Increment frame counter
            self.frame_count += 1
            await asyncio.sleep(1/fps)
            sleep(0.1)
            output_path = f"assets/frames/frame{self.frame_count-1}.jpg"
            # _, buffer = cv2.imencode('.jpg', frame)  # Encode frame as JPEG
            # frame_bytes = base64.b64encode(buffer)  # Convert frame to base64
            
            yield
            
            # return frame_bytes


def index() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.image(src="/logo.png", width="260px", height="auto", margin_left="30px", margin_top="23px"),
        ),
        rx.button(
            "Start", on_click=State.analyze_video
        ),
        rx.hstack(
            rx.vstack(
                rx.heading("Live Procedure", margin_top="10px", margin_left="30px", margin_bottom="15px", font_size="30px"),
                rx.image(src=State.output_path, width="520", height="auto", margin_left="30px", margin_top="23px"), # LIVE STREAM
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
        #rx.text(response.text)
    )

app = rx.App(style=style)
app.add_page(index)
