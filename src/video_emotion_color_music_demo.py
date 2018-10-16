from statistics import mode
import __future__
import cv2
from keras.models import load_model
import numpy as np


import sys

from utils.datasets import get_labels
from utils.inference import detect_faces
from utils.inference import draw_text
from utils.inference import draw_bounding_box
from utils.inference import apply_offsets
from utils.inference import load_detection_model
from utils.preprocessor import preprocess_input

import mood_player

angry_playlist = '/home/jbc/Projects/emotion_music_player/src/Playlist/angry_list'
sad_playlist = '/home/jbc/Projects/emotion_music_player/src/Playlist/sad_list'
surprise_playlist = '/home/jbc/Projects/emotion_music_player/src/Playlist/surprise_list'
happy_playlist = '/home/jbc/Projects/emotion_music_player/src/Playlist/happy_list'

FRAME_LIST_LENGTH = 20
TOLERANCE = 0.5 #tolerance for false detection, a float < 1

# parameters for loading data and images
detection_model_path = '../trained_models/detection_models/haarcascade_frontalface_default.xml'
emotion_model_path = '../trained_models/emotion_models/fer2013_mini_XCEPTION.102-0.66.hdf5'
emotion_labels = get_labels('fer2013')

# hyper-parameters for bounding boxes shape
frame_window = 10
emotion_offsets = (20, 40)

# loading models
face_detection = load_detection_model(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)

# getting input model shapes for inference
emotion_target_size = emotion_classifier.input_shape[1:3]

# starting lists for calculating modes
emotion_window = []

# starting video streaming
cv2.namedWindow('window_frame')
video_capture = cv2.VideoCapture(0)

frame_count = 0
emotion_list = []
while True:
    bgr_image = video_capture.read()[1]
    gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
    rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
    faces = detect_faces(face_detection, gray_image)

    for face_coordinates in faces:

        x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
        gray_face = gray_image[y1:y2, x1:x2]
        try:
            gray_face = cv2.resize(gray_face, (emotion_target_size))
        except:
            continue

        gray_face = preprocess_input(gray_face, True)
        gray_face = np.expand_dims(gray_face, 0)
        gray_face = np.expand_dims(gray_face, -1)
        emotion_prediction = emotion_classifier.predict(gray_face)
        emotion_probability = np.max(emotion_prediction)
        emotion_label_arg = np.argmax(emotion_prediction)
        emotion_text = emotion_labels[emotion_label_arg]
        emotion_window.append(emotion_text)

        emotion_list.append(emotion_text)

        if len(emotion_window) > frame_window:
            emotion_window.pop(0)
        try:
            emotion_mode = mode(emotion_window)
        except:
            continue

        if emotion_text == 'angry':
            color = emotion_probability * np.asarray((255, 0, 0))
        elif emotion_text == 'sad':
            color = emotion_probability * np.asarray((0, 0, 255))
        elif emotion_text == 'happy':
            color = emotion_probability * np.asarray((255, 255, 0))
        elif emotion_text == 'surprise':
            color = emotion_probability * np.asarray((0, 255, 255))
        else:
            color = emotion_probability * np.asarray((0, 255, 0))

        color = color.astype(int)
        color = color.tolist()

        draw_bounding_box(face_coordinates, rgb_image, color)
        draw_text(face_coordinates, rgb_image, emotion_mode,
                  color, 0, -45, 1, 1)

        #print(emotion_mode)

        # when emotion_list reaches capacity, check the emotions, play corresponding music and clear the sampling list
        frame_count += 1

        if frame_count == FRAME_LIST_LENGTH+1:
            if emotion_list.count('angry')>= round((1-TOLERANCE)*FRAME_LIST_LENGTH):
                mood_player.m_player('angry',angry_playlist)
            if emotion_list.count('sad')>= round((1-TOLERANCE)*FRAME_LIST_LENGTH):
                mood_player.m_player('sad',sad_playlist)
            if emotion_list.count('neutral')>= round((1-TOLERANCE)*FRAME_LIST_LENGTH):
                mood_player.m_player('neutral',happy_playlist)
            if emotion_list.count('surprise')>= round((1-0.8)*FRAME_LIST_LENGTH):
                mood_player.m_plaer('surprise',surprise_playlist)

            del emotion_list[:]
            frame_count = 0

    bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    cv2.imshow('window_frame', bgr_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
