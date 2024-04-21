import asyncio
import cv2
from concurrent.futures import ThreadPoolExecutor
import google.generativeai as genai
import json
import PIL.Image
import os

async def gemini_call_async(output_folder, frame_count, frame_interval, model, executor):
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
    
    prompt = "Explain the image in 3 lines"
    
    # Asynchronously handle image processing and model invocation
    def process_image():
        img = PIL.Image.open(f"{output_folder}/frame_{frame_count // frame_interval}.jpg")
        return model.generate_content([prompt, img], safety_settings=safe)

    response = await asyncio.get_event_loop().run_in_executor(executor, process_image)
    print(response.text)
    return response.text


async def capture_frames_from_video_async(video_path, output_folder, interval_sec, model, executor):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Unable to open video file '{video_path}'")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval_sec)
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # cv2.imshow("Video Playback", frame)
        if frame_count % frame_interval == 0:
            output_path = f"{output_folder}/frame_{frame_count // frame_interval}.jpg"
            cv2.imwrite(output_path, frame)
            print(f"Saved frame {frame_count // frame_interval}")
            response = await asyncio.create_task(gemini_call_async(output_folder, frame_count, frame_interval, model, executor))
            # print(response)
            yield response

        frame_count += 1
        await asyncio.sleep(1 / fps if fps > 0 else 0.033)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

async def analyze_video_async(video_path):
    json_file_path = 'env.json'
    with open(json_file_path, 'r') as file:
        config = json.load(file)
        google_api_key = config['GOOGLE_API_KEY']

    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel('gemini-pro-vision')
    output_folder = "captured_frames"
    interval_sec = 5

    os.makedirs(output_folder, exist_ok=True)

    executor = ThreadPoolExecutor(max_workers=4)
    try:
        async for response in capture_frames_from_video_async(video_path, output_folder, interval_sec, model, executor):
            yield response
    finally:
        executor.shutdown()

if __name__ == "__main__":
    asyncio.run(analyze_video_async('path_to_video.mp4'))
