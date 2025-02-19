import cv2
from fer import FER
import time
import numpy as np

def initialize_camera(camera_id=0):
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        raise ValueError("Failed to open camera")
    return cap

def process_frame(frame, detector):
    # Flip the frame horizontally for selfie view
    frame = cv2.flip(frame, 1)
    
    # Detect emotions
    results = detector.detect_emotions(frame)
    
    if results:
        emotions = results[0]["emotions"]
        emotion, score = max(emotions.items(), key=lambda item: item[1])
        
        # Draw a more attractive display
        overlay = frame.copy()
        # Add background rectangle for text
        cv2.rectangle(overlay, (30, 20), (300, 70), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
        
        # Display emotion with confidence
        text = f"{emotion}: {score:.2f}"
        cv2.putText(frame, text, (40, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, 
                   (255, 255, 255), 2)
        
        # Draw face rectangle
        box = results[0]["box"]
        cv2.rectangle(frame, 
                     (box[0], box[1]), 
                     (box[0] + box[2], box[1] + box[3]), 
                     (0, 255, 0), 2)
    
    return frame

def main():
    try:
        # Initialize detector and camera
        detector = FER(mtcnn=True)
        cap = initialize_camera()
        
        # Track FPS
        fps_start_time = time.time()
        fps_counter = 0
        fps = 0
        
        print("Press 'q' to exit | Press 's' to save snapshot")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break
                
            # Process frame
            processed_frame = process_frame(frame, detector)
            
            # Calculate and display FPS
            fps_counter += 1
            if (time.time() - fps_start_time) > 1:
                fps = fps_counter
                fps_counter = 0
                fps_start_time = time.time()
            
            cv2.putText(processed_frame, f"FPS: {fps}", 
                       (processed_frame.shape[1] - 120, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, 
                       (0, 255, 0), 2)
            
            # Display frame
            cv2.imshow("Emotion Detector", processed_frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                cv2.imwrite(f"emotion_snapshot_{timestamp}.jpg", processed_frame)
                print(f"Snapshot saved: emotion_snapshot_{timestamp}.jpg")
                
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
