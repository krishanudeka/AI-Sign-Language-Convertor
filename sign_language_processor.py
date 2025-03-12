import cv2
import numpy as np
import mediapipe as mp # type: ignore

mp_hands = mp.solutions.hands

def process_sign_language(image_file):
    hands = mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=2,
        min_detection_confidence=0.7
    )
    
    try:
        # Convert image file to numpy array
        file_bytes = np.frombuffer(image_file.read(), np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        if image is None:
            return {'error': 'Invalid image file'}, 400

        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process the image
        results = hands.process(image_rgb)
        
        if not results.multi_hand_landmarks:
            return {'text': '', 'confidence': 0}

        # Process hand landmarks
        landmarks = results.multi_hand_landmarks[0]
        
        # Get finger positions
        thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
        index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        
        # Calculate proper Euclidean distance
        distance = np.sqrt(
            (thumb_tip.x - index_tip.x)**2 + 
            (thumb_tip.y - index_tip.y)**2
        )
        
        # Improved detection logic
        if distance < 0.1:
            return {'text': 'Hello', 'confidence': max(0.8, 1 - distance*5)}
        else:
            return {'text': 'Thank You', 'confidence': max(0.7, distance*2)}
            
    except Exception as e:
        raise Exception(f"Image processing error: {str(e)}")
    finally:
        hands.close()
