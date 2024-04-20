import cv2
from time import sleep

def capture_frames_from_video(video_path, output_folder, interval_sec):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video file was opened successfully
    if not cap.isOpened():
        print(f"Error: Unable to open video file '{video_path}'")
        return

    # Get the frame rate of the video
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Calculate frame interval based on desired interval_sec
    frame_interval = int(fps * interval_sec)

    # Initialize frame counter
    frame_count = 0

    try:
        while True:
            # Read a frame from the video
            ret, frame = cap.read()

            if not ret:
                break  # Break the loop if we've reached the end of the video

            # Display the current frame (video playback)
            cv2.imshow("Video Playback", frame)

            # Check if it's time to save a frame
            if frame_count % frame_interval == 0:
                # Save the frame as an image file
                output_path = f"{output_folder}/frame_{frame_count // frame_interval}.jpg"
                cv2.imwrite(output_path, frame)
                print(f"Saved frame {frame_count // frame_interval}")

            # Increment frame counter
            frame_count += 1
            #if (fps != 0):
            sleep(1/fps)

            # Check for key press (press 'q' to stop playback)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        # Release the video capture object and close any open windows
        cap.release()
        cv2.destroyAllWindows()

'''Main function to be called
'''
def analyze_video(video_path):
    output_folder = "captured_frames"  # Output folder to save captured frames
    interval_sec = 1  # Interval in seconds to capture frames

    # Create the output folder if it doesn't exist
    import os
    os.makedirs(output_folder, exist_ok=True)

    # Call the function to capture frames from the video
    capture_frames_from_video(video_path, output_folder, interval_sec)
