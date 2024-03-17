import cv2
import numpy as np
from pathlib import Path

# Install required libraries (if not already installed)
# Use a package manager like pip: pip install opencv-python pytesseract yolov8

def preprocess_image(img):
    # Convert to BGR format for OpenCV
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img

def detect_plates(model, frame):
    results = model(frame)
    plates = []  # Store detected plates

    # Extract data from detections with confidence above a threshold
    for detection in results.pandas().xyxy[0]:
        if detection['name'] == 'license_plate' and detection['confidence'] > 0.5:
            x_min, y_min, x_max, y_max, conf, class_id = detection
            plate_img = frame[int(y_min):int(y_max), int(x_min):int(x_max)]
            plates.append((plate_img, (x_min, y_min, x_max, y_max)))

    return plates

def extract_text(plate_img):
    # Preprocess for text extraction (optional based on image quality)
    # Convert to grayscale
    gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
    # Apply thresholding (adjust threshold as needed)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # Deskew for better OCR (adjust deskewing parameters as needed)
    _, contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        cnt = contours[0]
        rect = cv2.boundingRect(cnt)
        x, y, w, h = rect
        angle = cv2.rotatedRectAngles(cv2.minAreaRect(cnt))[0]
        if angle < -45:
            angle += 90
        elif angle > 45:
            angle -= 90
        rotated = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
        plate_img = cv2.warpAffine(thresh, rotated, (w, h))

    # Use Tesseract for OCR (ensure Tesseract is installed and configured)
    text = pytesseract.image_to_string(plate_img, config='--psm 10')
    return text

def save_to_csv(data, filename):
    # Create CSV file with headers
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Frame', 'Plate Text', 'Bounding Box (x_min, y_min, x_max, y_max)'])

        # Write data to CSV
        for frame_num, plate_text, box in data:
            writer.writerow([frame_num, plate_text, box])

if __name__ == '__main__':
    # Replace with your YOLOv8 model path and class names file path
    model_path = 'path/to/yolov8.pt'
    class_names_path = 'path/to/yolov8.names'

    # Load YOLOv8 model
    model = torch.hub.load('ultralytics/yolov8', 'yolov8s', pretrained=True)
    model.conf = 0.5  # Adjust confidence threshold as needed
    model.iou = 0.45  # Adjust IoU threshold as needed

    # Load class names
    with open(class_names_path, 'r') as f:
        class_names = [line.strip() for line in f.readlines()]

    # Specify video path
    video_path = 'path/to/your/video.mp4'

    # Open video capture
    cap = cv2.VideoCapture(video_path)

    # Create CSV filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_filename = f'number_plates
