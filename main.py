import cv2
import mediapipe as mp
import numpy as np
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
app.mount('/class_audio', StaticFiles(directory='class_audio'), name='class_audio')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True)

# نقاط العين اليسرى واليمنى حسب MediaPipe FaceMesh
LEFT_EYE_IDX = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_IDX = [362, 385, 387, 263, 373, 380]

def eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

EYE_AR_THRESH = 0.23

@app.get('/', response_class=HTMLResponse)
def index():
    with open('static/index.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.post('/detect')
def detect_drowsiness(file: UploadFile = File(...)):
    image_bytes = file.file.read()
    npimg = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)
    drowsy = False
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = np.array([(lm.x * frame.shape[1], lm.y * frame.shape[0]) for lm in face_landmarks.landmark])
            leftEye = landmarks[LEFT_EYE_IDX]
            rightEye = landmarks[RIGHT_EYE_IDX]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0
            if ear < EYE_AR_THRESH:
                drowsy = True
    return {"drowsy": drowsy}

if __name__ == '__main__':
    import uvicorn
    import os
    ssl_keyfile = 'key.pem'
    ssl_certfile = 'cert.pem'
    if os.path.exists(ssl_keyfile) and os.path.exists(ssl_certfile):
        uvicorn.run(
            'main:app',
            host='0.0.0.0',
            port=8000,
            reload=True,
            ssl_keyfile=ssl_keyfile,
            ssl_certfile=ssl_certfile
        )
    else:
        uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True) 