from videocapture import analyze_video_async
import asyncio

# video_path = "StitchWitch/sample-video.mp4"  # Path to the desired video
video_path = "data/video/lumbar_discectomy.mp4"  # Path to the desired video

# Ensures the async function is called and awaited properly
if __name__ == "__main__":
    asyncio.run(analyze_video_async(video_path))