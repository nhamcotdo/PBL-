from flask import Flask, send_file
from flask_cors import cross_origin
from flask import request
from flask import jsonify
import numpy as np
import requests
from io import BytesIO
import tempfile
import traceback
from LSTM_model import *
from redis import Redis

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

@app.route("/")
def hello():
  return "Hello World!"

@app.route('/LSTM', methods=['POST'])
@cross_origin(origin='*')
def LSTM_model():
    if request.method == 'POST':
        try:
            if 'video_file' not in request.files:
                return "The request must have path_file or video_file param", 400
            
            file = request.files['video_file']

            if file.filename == '':
                return "No file selected", 400
            
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                file.save(tmp.name)

            cap = cv2.VideoCapture(tmp.name)
            if not cap.isOpened():
                return 'Could not open video file', 400
            
            sequence = []
            sentence = []
            predictions = []


            # Set mediapipe model
            with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
                while cap.isOpened():

                    # Read feed
                    ret, frame = cap.read()
                    if not ret:
                        break

                    # Make detections
                    image, results = mediapipe_detection(frame, holistic)

                    # Draw landmarks
                    # draw_styled_landmarks(image, results)

                    # 2. Prediction logic
                    keypoints = extract_keypoints(results)
                    sequence.append(keypoints)
                    sequence = sequence[-sequence_length:]

                    if len(sequence) == sequence_length:
                        res = model.predict(np.expand_dims(sequence, axis=0))[0]
                        print(actions[np.argmax(res)])
                        print(res)
                        predictions.append(np.argmax(res))

                        print(np.unique(predictions[-10:])[0])

                        if np.unique(predictions[-10:])[0] == np.argmax(res):
                            if res[np.argmax(res)] > threshold:

                                if len(sentence) > 0:
                                    if actions[np.argmax(res)] != sentence[-1]:
                                        sentence.append(actions[np.argmax(res)])
                                else:
                                    sentence.append(actions[np.argmax(res)])

                    # cv2.rectangle(image, (0, 0), (640, 40), (245, 117, 16), -1)
                    # cv2.putText(image, ' '.join(sentence), (3, 20),
                    #             cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                    # Show to screen
                    # cv2.imshow('OpenCV Feed', image)

                    # Break gracefully
                    # if cv2.waitKey(1) & 0xFF == ord('q'):
                        # break

                cap.release()
                cv2.destroyAllWindows()

            return ' '.join(sentence)
            
        except Exception as e:
            error = "'Error': '" + str(e) + "'"
            print(error)

            traceback.print_exc()

            return error, 400

if __name__ == "__main__":
    model = LSTMModel('./weights/weightsnewdata.h5')
    app.run(debug=True, port=5001, host="0.0.0.0")