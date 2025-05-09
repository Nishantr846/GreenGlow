from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import numpy as np
from PIL import Image
import tensorflow as tf
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Load your trained model
model = tf.keras.models.load_model('trained_model.h5')  # Ensure this path is correct
print("Model input shape:", model.input_shape)
class_names = ['Apple___Apple_scab',
 'Apple___Black_rot',
 'Apple___Cedar_apple_rust',
 'Apple___healthy',
 'Blueberry___healthy',
 'Cherry_(including_sour)___Powdery_mildew',
 'Cherry_(including_sour)___healthy',
 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
 'Corn_(maize)___Common_rust_',
 'Corn_(maize)___Northern_Leaf_Blight',
 'Corn_(maize)___healthy',
 'Grape___Black_rot',
 'Grape___Esca_(Black_Measles)',
 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
 'Grape___healthy',
 'Orange___Haunglongbing_(Citrus_greening)',
 'Peach___Bacterial_spot',
 'Peach___healthy',
 'Pepper,_bell___Bacterial_spot',
 'Pepper,_bell___healthy',
 'Potato___Early_blight',
 'Potato___Late_blight',
 'Potato___healthy',
 'Raspberry___healthy',
 'Soybean___healthy',
 'Squash___Powdery_mildew',
 'Strawberry___Leaf_scorch',
 'Strawberry___healthy',
 'Tomato___Bacterial_spot',
 'Tomato___Early_blight',
 'Tomato___Late_blight',
 'Tomato___Leaf_Mold',
 'Tomato___Septoria_leaf_spot',
 'Tomato___Spider_mites Two-spotted_spider_mite',
 'Tomato___Target_Spot',
 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
 'Tomato___Tomato_mosaic_virus',
 'Tomato___healthy']  # Your class labels

@app.route('/')
def index():
    return render_template('index.html')  # Your main upload page

# Optional pages for navigation
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

care_tips = {
    'Apple___Apple_scab': "Remove and destroy infected leaves. Apply fungicides during the growing season.",
    'Apple___Black_rot': "Prune out dead branches and remove mummified fruit. Use appropriate fungicides.",
    'Apple___Cedar_apple_rust': "Remove nearby cedar trees if possible. Apply fungicides during apple tree bloom.",
    'Apple___healthy': "Maintain regular watering and fertilization. Monitor for pests and diseases.",
    'Blueberry___healthy': "Ensure proper soil pH and mulch to retain moisture.",
    'Cherry_(including_sour)___Powdery_mildew': "Prune to increase air circulation. Apply fungicides if needed.",
    'Cherry_(including_sour)___healthy': "Water regularly and mulch to conserve moisture.",
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': "Rotate crops and use resistant varieties. Apply fungicides if necessary.",
    'Corn_(maize)___Common_rust_': "Plant resistant hybrids and apply fungicides if needed.",
    'Corn_(maize)___Northern_Leaf_Blight': "Use resistant hybrids and practice crop rotation.",
    'Corn_(maize)___healthy': "Maintain soil fertility and monitor for pests.",
    'Grape___Black_rot': "Remove mummified fruit and prune infected canes. Apply fungicides.",
    'Grape___Esca_(Black_Measles)': "Prune out infected wood and apply fungicides.",
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': "Remove infected leaves and apply fungicides.",
    'Grape___healthy': "Ensure proper irrigation and nutrient management.",
    'Orange___Haunglongbing_(Citrus_greening)': "Remove infected trees and control psyllid vectors.",
    'Peach___Bacterial_spot': "Use resistant varieties and apply copper sprays.",
    'Peach___healthy': "Maintain good sanitation and proper fertilization.",
    'Pepper,_bell___Bacterial_spot': "Remove infected plants and avoid overhead watering.",
    'Pepper,_bell___healthy': "Provide consistent watering and fertilization.",
    'Potato___Early_blight': "Remove and destroy infected plants. Apply fungicides early.",
    'Potato___Late_blight': "Use resistant varieties and apply fungicides regularly.",
    'Potato___healthy': "Rotate crops and maintain soil health.",
    'Raspberry___healthy': "Prune properly and monitor for pests.",
    'Soybean___healthy': "Ensure proper planting density and nutrient management.",
    'Squash___Powdery_mildew': "Remove infected leaves and apply fungicides.",
    'Strawberry___Leaf_scorch': "Remove infected leaves and avoid overhead irrigation.",
    'Strawberry___healthy': "Maintain proper soil moisture and fertilization.",
    'Tomato___Bacterial_spot': "Remove infected plants and avoid overhead watering.",
    'Tomato___Early_blight': "Use resistant varieties and apply fungicides.",
    'Tomato___Late_blight': "Apply fungicides and remove infected plants.",
    'Tomato___Leaf_Mold': "Increase air circulation and apply fungicides.",
    'Tomato___Septoria_leaf_spot': "Remove infected leaves and apply fungicides.",
    'Tomato___Spider_mites Two-spotted_spider_mite': "Use miticides and encourage natural predators.",
    'Tomato___Target_Spot': "Remove infected leaves and apply fungicides.",
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus': "Control whiteflies and remove infected plants.",
    'Tomato___Tomato_mosaic_virus': "Use resistant varieties and sanitize tools.",
    'Tomato___healthy': "Provide balanced fertilization and regular watering."
}

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
            # Preprocess image
            image = Image.open(file_path)
            image = image.convert('RGB')
            image = image.resize((128, 128))
            image_array = np.expand_dims(np.array(image) / 255.0, axis=0)

            # Prediction
            prediction = model.predict(image_array)
            print("Prediction array:", prediction)
            predicted_class = class_names[np.argmax(prediction)]
            print("Predicted class:", predicted_class)

            tips = care_tips.get(predicted_class, "No care tips available for this disease.")

            return jsonify({'disease': predicted_class, 'care_tips': tips})
        except Exception as e:
            print("Error during prediction:", e)
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Unexpected error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
