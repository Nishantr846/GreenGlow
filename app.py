from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
import numpy as np
from PIL import Image
import tensorflow as tf  # or use joblib for sklearn models

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Load your model
model = tf.keras.models.load_model('model.h5')  # adjust path as needed
class_names = ['Healthy', 'Bacterial Spot', 'Early Blight', 'Late Blight']  # example classes

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

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        if 'image' not in request.files:
            return "No file part"
        file = request.files['image']
        if file.filename == '':
            return "No selected file"
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Preprocess the image
            image = Image.open(file_path).resize((224, 224))
            image_array = np.expand_dims(np.array(image) / 255.0, axis=0)

            # Make prediction
            prediction = model.predict(image_array)
            predicted_class = class_names[np.argmax(prediction)]

            return render_template('prediction_result.html', image_url=file_path, prediction=predicted_class)
    return render_template('predict.html')

if __name__ == '__main__':
    app.run(debug=True)
