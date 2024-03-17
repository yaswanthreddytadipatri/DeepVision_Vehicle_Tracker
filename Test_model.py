import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO("best_100_epochs.pt","mps")

# Open the video capture
cap = cv2.VideoCapture("Test_data/test4.mp4")

while True:
    # Read a frame from the video
    ret, frame = cap.read()

    # If the frame was not successfully read, break the loop
    if not ret:
        break

    # Detect objects in the frame
    results = model(frame)

    # Visualize the detected objects
    annotated_frame = results[0].plot()

    # Display the annotated frame
    cv2.imshow("Object Detection", annotated_frame)

    # Wait for the 'q' key to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the window
cap.release()
cv2.destroyAllWindows()