import logging
from logging.config import dictConfig
from logging.handlers import RotatingFileHandler
import os
from flask import Flask
from flask_cors import cross_origin
from flask import request
import numpy as np
import tempfile
import traceback
from LSTM_model import *
import subprocess


app = Flask(__name__)

logging.basicConfig(filename='logs.log', level=logging.INFO)
# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Create a file handler and set the formatter
file_handler = RotatingFileHandler('logs.log', maxBytes=10240, backupCount=10)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# Create a stream handler and set the formatter
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


@app.route("/")
def hello():
  return "Hello World!"

@app.route('/LSTM', methods=['POST'])
@cross_origin(origin='*')
def LSTM_model():
    if request.method == 'POST':
        try:
            logger.info('Start request')
            if 'video_file' not in request.files:
                return "The request must have path_file or video_file param", 400
            
            file = request.files['video_file']
            if file.filename == '':
                return "No file selected", 400
            
            save_folder = f'./files/'
            with tempfile.NamedTemporaryFile(delete=False, dir=save_folder) as tmp:
                file.save(tmp.name)
                
            cap = cv2.VideoCapture(tmp.name)

            if not cap.isOpened():
                return 'Could not open video file', 400
            
            sequence = []
            sentence = []
            predictions = []

            cap.set(cv2.CAP_PROP_XI_FRAMERATE, 20)
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
                    keypoints = keypoints / np.max([np.abs(keypoints), np.abs(keypoints)])
                    sequence.append(keypoints)
                    sequence = sequence[-sequence_length:]

                    if len(sequence) == sequence_length:
                        res = model.predict(np.expand_dims(sequence, axis=0))[0]
                        print(actions[np.argmax(res)])
                        print(res[np.argmax(res)])
                        predictions.append(np.argmax(res))

                        # print(np.unique(predictions[-10:])[0])

                        if np.unique(predictions[-10:])[0] == np.argmax(res):
                            if res[np.argmax(res)] > threshold:
                                sequence = []
                                if len(sentence) > 0:
                                    if actions[np.argmax(res)] != sentence[-1]:
                                        sentence.append(actions[np.argmax(res)])
                                        print(actions[np.argmax(res)])
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
                save_path = os.path.join(save_folder, file.filename)
                os.rename(tmp.name, save_path)
                rs = ' '.join(sentence)
                cv2.destroyAllWindows()

                f = open('result.json')
                results = json.load(f)
                f.close()
                results[save_path] = rs
                with open('result.json', 'w') as json_file:
                    json.dump(results, json_file)
                
            logger.info(f'Kết quả {rs}')
            logger.info('Done request')
            return rs or 'Không nhận dạng được'
            
        except Exception as e:
            error = "'Error': '" + str(e) + "'"
            print(error)

            traceback.print_exc()
            logger.error(e.with_traceback())

            return error, 400
@app.route('/LSTM/single', methods=['POST'])
@cross_origin(origin='*')
def LSTM_model_single():
    if request.method == 'POST':
        try:
            logger.info('Start request')
            if 'video_file' not in request.files:
                return "The request must have path_file or video_file param", 400
            
            file = request.files['video_file']

            if file.filename == '':
                return "No file selected", 400
            
            save_folder = f'./files/'
            with tempfile.NamedTemporaryFile(delete=False, dir=save_folder) as tmp:
                file.save(tmp.name)
                

            cap = cv2.VideoCapture(tmp.name)
            if not cap.isOpened():
                return 'Could not open video file', 400
            
            keypoints = frames_extraction(tmp.name)
            keypoints = keypoints / np.max([np.abs(keypoints), np.abs(keypoints)])
        
            if len(keypoints) == sequence_length:
                res = model.predict(np.reshape(keypoints, (1,  sequence_length, 300)))[0]
                word = actions[np.argmax(res)]
            
            save_path = os.path.join(save_folder, file.filename)
            os.rename(tmp.name, save_path)
            cv2.destroyAllWindows()

            f = open('result.json')
            results = json.load(f)
            f.close()
            results[save_path] = word
            with open('result.json', 'w') as json_file:
                json.dump(results, json_file)
            
            logger.info(f'Kết quả {word}')
            print(word)
            logger.info('Done request')
            return word or 'Không nhận dạng được'
            
        except Exception as e:
            error = "'Error': '" + str(e) + "'"
            print(error)

            traceback.print_exc()
            logger.error(e.with_traceback())

            return error, 400

if __name__ == "__main__":
    model = LSTMModel(setting['weight'])
    app.run(debug=False, port=5001, host="0.0.0.0")
