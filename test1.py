import cv2
import pandas as pd
from ultralytics import YOLO
import easyocr
import datetime

# Initialize YOLOv8 model
model = YOLO("best_100_epochs.pt")

# Initialize EasyOCR reader
reader = easyocr.Reader(["en"])

# Initialize CSV file
data = {"Text": [], "Date": [], "Duration": []}
df = pd.DataFrame(data)

# Open video file
# cap = cv2.VideoCapture("Test_data/test4.mp4")
cap = cv2.VideoCapture("/Users/yashwanth/Downloads/Traffic Flow In The Highway - 4K Stock Videos _ NoCopyright _ AllVideoFree.mp4")
# cap = cv2.VideoCapture(0)

# Initialize text tracking
current_text = ""
start_time = None

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        break

    # Detect objects using YOLOv8
    results = model(frame)

    # Extract text from detected objects
    for result in results:
        boxes = result.boxes.data.tolist()
        for box in boxes:
            x1, y1, x2, y2, conf, cls = [int(x) for x in box]
            cropped = frame[y1:y2, x1:x2]
            text = reader.recognize(cropped)

            if text:
                text = text[0][-2]
                if text != current_text:
                    if current_text:
                        end_time = datetime.datetime.now()
                        duration = end_time - start_time
                        df = df._append({"Text": current_text, "Date": start_time, "Duration": duration}, ignore_index=True)

                    current_text = text
                    start_time = datetime.datetime.now()
                else:
                    # Text is repeated, update duration
                    pass

                # Draw bounding box and display text
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36, 255, 12), 2)

                # Display confidence percentage
                conf_text = f" {conf * 100:.2f}%"
                cv2.putText(frame, conf_text, (x1, y1 - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36, 255, 12), 2)

    # Display the resulting frame
    cv2.imshow("Frame", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the video capture object
cap.release()
cv2.destroyAllWindows()

# Save CSV file
df.to_csv("output.csv", index=False)