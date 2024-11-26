# Import necessary libraries
import speech_recognition as sr
import spacy
import cv2

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Step 1: Speech Recognition
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please speak...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"Recognized text: {text}")
        return text
    except sr.UnknownValueError:
        print("Speech recognition could not understand the audio")
        return None
    except sr.RequestError:
        print("Error with the speech recognition service")
        return None

# Step 2: Text Processing (Simplify the text for sign translation)
def process_text(text):
    doc = nlp(text)
    simplified_text = " ".join([token.lemma_ for token in doc if not token.is_stop])
    print(f"Simplified text for sign language: {simplified_text}")
    return simplified_text

# Step 3: Display Hand Sign Images for Each Word
# Set up a dictionary that maps simplified words to corresponding images
sign_images = {
    "hello": "signs/hello.jpeg",
    "thank": "signs/thank.png",
    "you": "signs/you.png",
    # Add more words and corresponding sign images here
}

def display_signs(text):
    words = text.split()
    for word in words:
        if word in sign_images:
            image_path = sign_images[word]
            image = cv2.imread(image_path)
            if image is not None:
                cv2.imshow("Hand Sign", image)
                cv2.waitKey(5000)  # Display each sign for 1 second
            else:
                print(f"Image for '{word}' not found")
        else:
            print(f"No sign found for '{word}'")
    cv2.destroyAllWindows()

# Integrate all components into the voice-to-hand-sign function
def voice_to_hand_sign():
    # Recognize Speech
    text = recognize_speech()
    
    if text:
        # Process Text
        simplified_text = process_text(text)
        
        # Display Hand Signs
        display_signs(simplified_text)

# Run the voice-to-hand-sign translator
voice_to_hand_sign()
