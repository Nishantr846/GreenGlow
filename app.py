from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image

app = Flask(__name__)
model = load_model('model.h5')  # Ensure this path matches your downloaded model

# Define the class names based on your model's training
CLASS_NAMES = ['Apple Scab', 'Apple Black Rot', 'Grape Black Measles', 'Potato Early Blight', 'Healthy']

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    img = Image.open(file.stream).resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)[0]
    class_index = np.argmax(prediction)
    disease = CLASS_NAMES[class_index]

    return jsonify({'disease': disease})

if __name__ == '__main__':
    app.run(debug=True)
