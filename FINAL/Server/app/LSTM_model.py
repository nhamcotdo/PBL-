import tensorflow as tf
from Common import *

class LSTMModel:
    def __init__(self, weight_path, threshold = 0.4):
        self.threshold = threshold
        self.model = tf.keras.models.load_model(weight_path)

    def predict(self, sequence):
        return self.model.predict(sequence)
    # def video_predict(self, video_path):
    #     cap = cv2.VideoCapture(0)
    #     sequence = []
    #     sentence = []
    #     predictions = []


    #     cap = cv2.VideoCapture(video_path)
    #     # Set mediapipe model
    #     with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    #         while cap.isOpened():

    #             # Read feed
    #             ret, frame = cap.read()

    #             # Make detections
    #             image, results = mediapipe_detection(frame, holistic)

    #             # Draw landmarks
    #             # draw_styled_landmarks(image, results)

    #             # 2. Prediction logic
    #             keypoints = extract_keypoints(results)
    #             sequence.append(keypoints)
    #             sequence = sequence[-sequence_length:]

    #             if len(sequence) == sequence_length:
    #                 res = self.model.predict(np.expand_dims(sequence, axis=0))[0]
    #                 print(actions[np.argmax(res)])
    #                 predictions.append(np.argmax(res))

    #             # 3. Viz logic
    #                 if np.unique(predictions[-10:])[0] == np.argmax(res):
    #                     if res[np.argmax(res)] > self.threshold:

    #                         if len(sentence) > 0:
    #                             if actions[np.argmax(res)] != sentence[-1]:
    #                                 sentence.append(actions[np.argmax(res)])
    #                         else:
    #                             sentence.append(actions[np.argmax(res)])

    #             cv2.rectangle(image, (0, 0), (640, 40), (245, 117, 16), -1)
    #             cv2.putText(image, ' '.join(sentence), (3, 20),
    #                         cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    #             # Show to screen
    #             # cv2.imshow('OpenCV Feed', image)

    #             # Break gracefully
    #             # if cv2.waitKey(1) & 0xFF == ord('q'):
    #                 # break

    #         cap.release()
    #         cv2.destroyAllWindows()

    #     return sentence.join(' ')
                        