# SmartCam AI Classifier

SmartCam AI Classifier is a high-fidelity web application powered by Flask and TensorFlow's Teachable Machine, featuring a custom neo-brutalist UI design.

## Features

- **Exact Design Fidelity:** Implements the provided Stitch design natively using HTML, Tailwind CSS, and Vanilla JavaScript.
- **Teachable Machine Integration:** Loads and runs `keras_model.h5` efficiently using `tf_keras`.
- **Dynamic Labels:** Automatically reads `labels.txt` to support dynamic classification schemas without code changes.
- **Rich Confidence Analysis:** Animated progress bars, dynamic color-coding (Green for Very High confidence, Blue for Moderate, Orange for Low), and dynamically generated AI Insights based on prediction confidence.
- **AJAX Interactions:** Fully asynchronous image uploading and result rendering for a smooth single-page application experience.

## Project Structure

```
SmartCam_Project/
│
├── app.py                  # Main Flask application and ML logic
├── keras_model.h5          # Teachable Machine H5 Model File
├── labels.txt              # Model Class Labels
├── requirements.txt        # Python Dependencies
│
├── templates/
│   └── index.html          # Frontend HTML Template (based on Stitch design)
│
├── static/
│   ├── css/
│   │   └── style.css       # Custom neo-brutalist styles and animations
│   │
│   ├── js/
│   │   └── app.js          # AJAX and DOM manipulation logic
│   │
│   └── assets/
│       └── images/         # Placeholders for any static imagery
│
└── README.md               # Documentation
```

## Requirements

- Python 3.9+
- TensorFlow 2.16+
- tf_keras 2.16+
- Flask

## Installation

1. Install required dependencies:

```bash
pip install -r requirements.txt
```

2. Make sure `keras_model.h5` and `labels.txt` are in the project root directory.

## Usage

1. Start the Flask server:

```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`.
3. Drag and drop an image onto the upload zone, or click to browse local files.
4. View the instant, highly-detailed classification results.
