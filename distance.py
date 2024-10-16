import os
import cv2
import numpy as np

# Load YOLO-style labels from text files
def load_yolo_labels(labels_folder, image_folder):
    labels = {}
    for filename in os.listdir(labels_folder):
        if filename.endswith('.txt'):
            image_filename = filename.replace('.txt', '.jpg')  # Assuming image files are .jpg
            image_path = os.path.join(image_folder, image_filename)
            img = cv2.imread(image_path)
            if img is None:
                print(f"Warning: Could not read image {image_path}")
                continue
            h, w = img.shape[:2]

            # Open label file and extract bounding boxes
            with open(os.path.join(labels_folder, filename), 'r') as file:
                bboxes = []
                for line in file.readlines():
                    class_id, x_center, y_center, width, height = map(float, line.strip().split())
                    x1 = int((x_center - width / 2) * w)
                    y1 = int((y_center - height / 2) * h)
                    x2 = int((x_center + width / 2) * w)
                    y2 = int((y_center + height / 2) * h)
                    bbox = (x1, y1, x2, y2)
                    bboxes.append(bbox)
                    print(f"Loaded bbox {bbox} for {image_filename}")
                labels[image_filename] = bboxes
    return labels

# Calculate distances between forklifts
def calculate_distances(bboxes):
    distances = []
    for i in range(len(bboxes) - 1):
        x1, y1, x2, y2 = bboxes[i]
        cx1 = (x1 + x2) / 2
        cy1 = (y1 + y2) / 2
        x1_next, y1_next, x2_next, y2_next = bboxes[i + 1]
        cx2 = (x1_next + x2_next) / 2
        cy2 = (y1_next + y2_next) / 2
        distance = ((cx2 - cx1) ** 2 + (cy2 - cy1) ** 2) ** 0.5
        distances.append(distance)
    return distances

# Draw bounding boxes and distances on the frames
def draw_bboxes_and_distances(image, bboxes, distances):
    for bbox in bboxes:
        x1, y1, x2, y2 = bbox
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    for i, distance in enumerate(distances):
        x1, y1, x2, y2 = bboxes[i]
        x1_next, y1_next, x2_next, y2_next = bboxes[i + 1]
        cx1 = (x1 + x2) / 2
        cy1 = (y1 + y2) / 2
        cx2 = (x1_next + x2_next) / 2
        cy2 = (y1_next + y2_next) / 2
        mid_point = (int((cx1 + cx2) / 2), int((cy1 + cy2) / 2))
        cv2.putText(image, f"{distance:.2f}", mid_point, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

# Convert processed images to a video
def convert_images_to_video(input_folder, output_video, frame_rate):
    images = [img for img in os.listdir(input_folder) if img.endswith(".jpg")]
    images.sort()
    frame = cv2.imread(os.path.join(input_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(input_folder, image)))

    cv2.destroyAllWindows()
    video.release()

if __name__ == "__main__":
    # Paths
    labels_folder = '/Users/bsid24082/Documents/IIQ/forklict/yolo_labels'  # YOLO label (.txt) files
    frame_folder = '/Users/bsid24082/Documents/IIQ/forklict/collision1_frames'  # Images and XML files (frames)
    output_folder = '/Users/bsid24082/Documents/IIQ/forklict/processed_frames'  # Processed frames output
    output_video = '/Users/bsid24082/Documents/IIQ/forklict/processed_video.mp4'  # Output video
    frame_rate = 10  # Set frame rate for video

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Load YOLO labels
    labels = load_yolo_labels(labels_folder, frame_folder)
    print("Labels loaded successfully.")

    # Process each frame
    for image_filename, bboxes in labels.items():
        print(f"Processing {image_filename} with {len(bboxes)} bounding boxes.")
        image_path = os.path.join(frame_folder, image_filename)
        image = cv2.imread(image_path)
        if image is None:
            print(f"Warning: Could not read image {image_path}")
            continue
        distances = calculate_distances(bboxes)
        print(f"Distances: {distances}")
        draw_bboxes_and_distances(image, bboxes, distances)
        output_image_path = os.path.join(output_folder, image_filename)
        cv2.imwrite(output_image_path, image)

    # Convert processed frames back into a video
    convert_images_to_video(output_folder, output_video, frame_rate)
    print(f"Processed video saved as {output_video}")