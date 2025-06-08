from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import numpy as np
from PIL import Image
import tensorflow as tf
import json
from flask_cors import CORS
from tensorflow.keras.preprocessing import image

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Load trained model
model = tf.keras.models.load_model('model/plant_disease_model.h5')

# Load class label map
with open('model/class_indices.json', 'r') as f:
    class_indices = json.load(f)
class_names = [k for k, v in sorted(class_indices.items(), key=lambda item: item[1])]

# Define disease-to-care mapping
disease_guide = {
    "Healthy": {
        "status": "Healthy",
        "care_tips": "Ensure 6–8 hours of sunlight, water regularly, and use compost monthly."
    },
    "Tomato___Late_blight": {
        "status": "Infected",
        "cure": "Use copper-based fungicides. Remove and destroy affected leaves.",
        "care_tips": "Improve air circulation. Avoid overhead watering."
    },
    "Tomato___Leaf_Mold": {
        "status": "Infected",
        "cure": "Apply sulfur or neem-based organic fungicides.",
        "care_tips": "Avoid high humidity. Ensure good spacing between plants."
    },
    "Tomato___Septoria_leaf_spot": {
        "status": "Infected",
        "cure": "Apply chlorothalonil-based fungicides.",
        "care_tips": "Remove infected leaves and mulch around the base."
    },
    "Potato___Early_blight": {
        "status": "Infected",
        "cure": "Use fungicides containing mancozeb or chlorothalonil.",
        "care_tips": "Rotate crops and remove debris after harvest."
    },
    "Potato___Late_blight": {
        "status": "Infected",
        "cure": "Spray with metalaxyl-based fungicides.",
        "care_tips": "Avoid excessive watering. Destroy infected plants."
    },
    "Pepper_bell___Bacterial_spot": {
        "status": "Infected",
        "cure": "Apply copper-based bactericides weekly.",
        "care_tips": "Avoid leaf wetness. Use disease-free seeds."
    },
    "Apple___Apple_scab": {
        "status": "Infected",
        "cure": "Use captan or mancozeb fungicides.",
        "care_tips": "Remove fallen leaves and prune trees for airflow."
    },
    "Apple___Black_rot": {
        "status": "Infected",
        "cure": "Spray with thiophanate-methyl fungicides.",
        "care_tips": "Prune cankers and destroy infected fruit."
    },
    "Grape___Black_rot": {
        "status": "Infected",
        "cure": "Apply myclobutanil or mancozeb during growing season.",
        "care_tips": "Ensure airflow and remove infected clusters."
    },
    "Strawberry___Leaf_scorch": {
        "status": "Infected",
        "cure": "Use captan fungicide at first signs.",
        "care_tips": "Avoid overhead watering. Use resistant varieties."
    }
}

# Optional pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/indoor_plants')
def indoor_plants():
    return render_template('indoor_plants.html')

@app.route('/garden_plants')
def garden_plants():
    return render_template('garden_plants.html')

@app.route('/common_diseases')
def common_diseases():
    return render_template('common_diseases.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        try:
            print(f"Processing file: {file_path}") # Debug print
            # Preprocess image
            img = image.load_img(file_path, target_size=(224, 224))
            img_array = image.img_to_array(img) / 255.0
            image_array = np.expand_dims(img_array, axis=0)
            print(f"Image array shape: {image_array.shape}") # Debug print

            # Predict
            prediction = model.predict(image_array)
            print(f"Raw prediction: {prediction}") # Debug print
            confidence = float(np.max(prediction))
            predicted_class = class_names[np.argmax(prediction)]
            print(f"Predicted class: {predicted_class}") # Debug print

            result = disease_guide.get(predicted_class, disease_guide["Healthy"])

            return jsonify({
                "disease": predicted_class,
                "confidence": round(confidence, 4),
                "status": result["status"],
                "cure": result.get("cure", "N/A"),
                "care_tips": result["care_tips"]
            })
        except Exception as e:
            print("Prediction error:", e)
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Unexpected error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 7700))
    app.run(host='0.0.0.0', port=port)