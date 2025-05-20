# Drowsiness Detection API (Eye Closure Detection with MediaPipe)

A web-based system for detecting drowsiness (eye closure) using AI and Google MediaPipe, with an interactive web interface and audio alert when drowsiness is detected.

---

## Features

- Drowsiness detection by tracking eye closure using MediaPipe Face Mesh.
- Interactive web interface (HTML + JS) displaying video and alerts.
- Automatic audio alarm when drowsiness is detected.
- FastAPI-based API for receiving and analyzing images.

---

## Requirements

- Python 3.8 or newer
- pip

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## How to Run

1. **Start the server:**

   ```bash
   uvicorn main:app --reload
   ```

   Or run directly from the code:

   ```bash
   python main.py
   ```

2. **Open your browser at:**
   ```
   http://localhost:8000/
   ```

---

## Project Structure

- `main.py` : Main server code, API, and drowsiness detection logic.
- `requirements.txt` : Project dependencies.
- `static/` : Frontend files (HTML, CSS, JS).
  - `index.html` : Main web page.
  - `script.js` : JavaScript for capturing video and sending frames to the server.
  - `style.css` : UI styling.
- `class_audio/` : Audio files for alerts.
  - `output_audio.mp3` : Alarm sound when drowsiness is detected.

---

## How It Works

1. **Frontend** captures a frame from the webcam every second and sends it to the server.
2. **Server** analyzes the image using MediaPipe Face Mesh and calculates the Eye Aspect Ratio (EAR).
3. If the eyes are closed for a certain period (EAR below a threshold), the server responds that the person is drowsy.
4. **Frontend** displays an alert and plays an alarm sound automatically.

---

## Customization

- Change the alarm sound by replacing `class_audio/output_audio.mp3`.
- Adjust detection sensitivity by changing the `EYE_AR_THRESH` value in `main.py`.
- Modify the UI or add features easily in the `static/` folder.

---

## Notes

- The system processes one image per request (not a live video stream).
- MediaPipe Face Mesh is set to detect only one face (`max_num_faces=1`).
- To support multiple faces, change this option in the code.

---

## Thank you for using this system!
If you have any questions or suggestions, feel free to reach out. 