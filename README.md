# Air-Writing-and-Character-Recognition ✍️

Draw letters and numbers in the air using your index finger — our AI models recognize them in real-time.

> **Modern System Support**: This version is specially patched to work with **Python 3.12 and 3.13** on Windows.

---

## 🛠️ Step-by-Step Installation (Spoon-Fed)

### 1. Open your Terminal
On Windows, press the `Start` button, type **PowerShell**, and open it. Do **not** use "Git Bash" for these specific commands as some paths might differ.

### 2. Clone the Project
Copy and paste this into PowerShell:
```powershell
git clone https://github.com/Butcherboy7/airwriter
cd airwriter
```

### 3. Create a Virtual Environment
This keeps the project clean. Copy these two lines:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
> **Note**: If you get a "scripts disabled" error, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` and try the second line again.

### 4. Install the Modern Dependencies
```powershell
pip install opencv-python keyboard mediapipe numpy pygame tensorflow flask
```

### 5. Download the AI Tracking Model
The app needs these "brain" files in a `models` folder. Run this command to create the folder and download the tracking model:
```powershell
mkdir models -ErrorAction SilentlyContinue
python -c "import urllib.request; urllib.request.urlretrieve('https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task', 'models/hand_landmarker.task'); print('Model Ready!')"
```
> **Note**: This repo already contains the Alphabet and Digit recognition models in the `models/` folder.

### 6. Apply the Internal Fix (Required for Python 3.13)
I've provided a script to automatically fix a bug in the MediaPipe library on Windows. Run this:
```powershell
python patch_mediapipe.py
```

### 7. Run the App!
```powershell
python app.py
```

Now, go to your browser and open: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🎮 Finger Controls

- **Index Finger (☝️)**: Start drawing on the screen.
- **Index + Middle (✌️)**: "Selection Mode" — use this to move your cursor without drawing (to select colors or erase).
- **Keyboard A**: Alphabet Recognition.
- **Keyboard N**: Number Recognition.
- **Keyboard O**: Turn recognition OFF (Standard Paint).

---

## 🔧 Behind the Scenes
I had to perform significant engineering to make this compatible with Python 3.13, including re-writing the tracking module and patching the core MediaPipe C-bindings. Full details are in [PROJECT_ISSUES_AND_SOLUTIONS.md](./PROJECT_ISSUES_AND_SOLUTIONS.md).
