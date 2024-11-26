import speech_recognition as sr

def capture_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        
    try:
        text = recognizer.recognize_google(audio)
        print(f"Recognized text: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("Could not understand the audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None


gesture_map = {
    "hello": "hello_gesture",
    "thanks": "thanks_gesture",
    "yes": "thumbs_up",
    "no": "thumbs_down"
    # Add more mappings as needed
}

def text_to_gesture(text):
    gesture = gesture_map.get(text, None)
    if gesture:
        print(f"Gesture for '{text}': {gesture}")
        return gesture
    else:
        print("No gesture mapping found for this text")
        return None


import mediapipe as mp
import cv2

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def display_gesture(gesture):
    # Initialize MediaPipe Hands
    hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.7)

    cap = cv2.VideoCapture(0)
    print("Press 'q' to exit")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Flip the frame to create a mirror image
        frame = cv2.flip(frame, 1)

        # Convert the image color to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame and find hand landmarks
        result = hands.process(rgb_frame)
        
        # Draw landmarks if hands are detected
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
        # Display the text for the current gesture
        cv2.putText(frame, f"Gesture: {gesture}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        
        cv2.imshow("Hand Gesture Display", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    hands.close()

def voice_to_hand_sign():
    # Capture the voice input
    text = capture_voice()
    
    if text:
        # Map the text to a hand gesture
        gesture = text_to_gesture(text)
        
        if gesture:
            # Display the mapped gesture
            display_gesture(gesture)

# Run the function
voice_to_hand_sign()
