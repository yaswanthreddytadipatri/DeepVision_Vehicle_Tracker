import cv2
import numpy as np
import pytesseract
import csv
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO("best_100_epochs.pt")  # Replace with your YOLOv8 model path

# Open the video capture
cap = cv2.VideoCapture("Test_data/test4.mp4")  # Replace with your video file path

# Open webcam
# cap = cv2.VideoCapture(0)

# Open the CSV file for writing
csv_file = open("detected_text.csv", "w", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Frame", "Text"])

frame_count = 0

while True:
    # Read a frame from the video
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # Detect objects in the frame
    results = model(frame)

    # Iterate through the detected objects
    for result in results:
        boxes = result.boxes
        for box in boxes:
            # Get the bounding box coordinates
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            # Extract the region of interest (ROI) from the frame
            roi = frame[y1:y2, x1:x2]

            # Convert the ROI to grayscale
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

            # Use Pytesseract to extract text from the ROI
            text = pytesseract.image_to_string(gray)
            if text:
                print(f"Frame {frame_count}: Detected Text: {text}")

                # Draw the bounding box and text on the frame
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36, 255, 12), 2)

                # Append the text to the CSV file
                csv_writer.writerow([frame_count, text])

    # Display the frame with bounding boxes and text
    cv2.imshow("YOLOv8 Object Detection", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
csv_file.close()