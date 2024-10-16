import cv2
import os

# Function to extract frames from a video and save them to a specified folder
def extract_frames(video_path, output_folder):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    count = 0

    while True:
        ret, frame = cap.read()

        # If a frame was successfully read
        if ret:
            # Save the frame as a JPEG file
            frame_name = os.path.join(output_folder, f"frame_{count:04d}.jpg")
            cv2.imwrite(frame_name, frame)
            count += 1
        else:
            break

    # Release the video capture object
    cap.release()

# Paths to the video files
video1_path = "/Users/bsid24082/Documents/June-July/horizontal_forklift/collision1.mp4"
video2_path = "/Users/bsid24082/Documents/June-July/horizontal_forklift/collision2.mp4"

# Output folders for extracted frames
output_folder1 = "/Users/bsid24082/Documents/June-July/horizontal_forklift/collision1_frames"
output_folder2 = "/Users/bsid24082/Documents/June-July/horizontal_forklift/collision2_frames"

# Extract frames from both videos
extract_frames(video1_path, output_folder1)
extract_frames(video2_path, output_folder2)

print("Frame extraction complete.")