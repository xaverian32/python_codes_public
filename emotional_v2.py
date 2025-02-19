import cv2
from deepface import DeepFace

# Function to detect emotion
def detect_emotion(frame):
    try:
        # Analyze the frame using DeepFace
        analysis = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
        
        # Handle if the result is a list or a dictionary
        if isinstance(analysis, list):
            analysis = analysis[0]  # Extract the first result if it's a list
        
        # Extract the dominant emotion
        emotion = analysis.get("dominant_emotion", "Unknown")
        return emotion
    except Exception as e:
        print(f"Error: {e}")
        return None

# Initialize the webcam
cap = cv2.VideoCapture(0)

print("Press 'q' to exit the camera feed.")
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # Flip the frame horizontally for a selfie view
    frame = cv2.flip(frame, 1)

    # Get the emotion detected
    emotion = detect_emotion(frame)

    # Display the emotion on the frame
    if emotion:
        cv2.putText(frame, f"Emotion: {emotion}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow("Emotion Detector", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()
