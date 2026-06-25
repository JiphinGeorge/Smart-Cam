import os
import io
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify, render_template
import tf_keras as keras

app = Flask(__name__)

# Load model and labels at startup
model = None
class_names = []

def load_model_and_labels():
    global model, class_names
    try:
        model = keras.models.load_model("keras_model.h5", compile=False)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        
    try:
        with open("labels.txt", "r") as f:
            class_names = [line.strip().split(" ", 1)[1] for line in f.readlines() if line.strip()]
        print("Labels loaded successfully.")
    except Exception as e:
        print(f"Error loading labels: {e}")

load_model_and_labels()

def preprocess_image(image):
    # Resize to 224x224
    image = image.resize((224, 224))
    
    # Convert grayscale to RGB, remove alpha
    if image.mode != 'RGB':
        image = image.convert('RGB')
        
    # Convert to numpy array
    image_array = np.asarray(image)
    
    # Normalize
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    
    # Shape to (1, 224, 224, 3)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array
    
    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None or not class_names:
        return jsonify({"error": "Model or labels not loaded properly"}), 500
        
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    try:
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        processed_data = preprocess_image(image)
        
        prediction = model.predict(processed_data)
        
        # Determine class
        pred_index = np.argmax(prediction)
        predicted_class = class_names[pred_index]
        confidence = float(prediction[0][pred_index]) * 100
        
        all_scores = []
        for i, score in enumerate(prediction[0]):
            all_scores.append({
                "id": i,
                "label": class_names[i] if i < len(class_names) else f"Class {i}",
                "score": float(score) * 100,
                "raw_value": float(score)
            })
            
        # Sort scores by highest first
        all_scores.sort(key=lambda x: x['score'], reverse=True)
        
        # AI Insight Logic
        if confidence >= 90:
            insight = f"The model is highly confident that this image belongs to the {predicted_class} class."
            confidence_level = "Very High"
        elif confidence >= 70:
            insight = f"The model believes this image is {predicted_class}, but confidence is moderate."
            confidence_level = "Moderate"
        else:
            insight = "The image is ambiguous. Consider using a clearer image."
            confidence_level = "Low"
            
        return jsonify({
            "predicted_class": predicted_class,
            "confidence": confidence,
            "all_scores": all_scores,
            "confidence_level": confidence_level,
            "insight": insight,
            "predicted_index": int(pred_index)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)