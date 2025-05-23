# GreenGlow - Your Plant's Guide

This project is a web application that uses a trained deep learning model to predict plant leaf diseases from uploaded images. It provides disease diagnosis and care tips to help users manage plant health effectively.

## Features

- Upload images of plant leaves to detect diseases.
- Predicts multiple types of diseases across various plants including apple, blueberry, cherry, corn, grape, orange, peach, pepper, potato, raspberry, soybean, squash, strawberry, and tomato.
- Provides care tips for each detected disease.
- Multiple informative pages including indoor plants, garden plants, common diseases, and about us.
- Built with Flask and TensorFlow for easy deployment.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Nishantr846/GreenGlow.git
   cd GreenGlow
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Open your web browser and navigate to:
   ```
   https://greenglow-your-plants-guide.onrender.com/
   ```

2. Use the web interface to upload images of plant leaves and get disease predictions along with care tips.

## Project Structure

- `app.py` - Main Flask application file containing routes and prediction logic.
- `trained_model.h5` - Pre-trained TensorFlow model used for disease prediction.
- `requirements.txt` - Python dependencies.
- `templates/` - HTML templates for different pages.
- `static/` - Static files including CSS, JavaScript, images, and uploaded files.
- `Test_Plant_Disease.ipynb` - Notebook for testing the model.
- `Train_plant_disease.ipynb` - Notebook for training the model.
- `training_hist.json` - Training history of the model.

## Model Details

The model predicts the following classes of plant diseases and healthy states:

- Apple: Apple scab, Black rot, Cedar apple rust, Healthy
- Blueberry: Healthy
- Cherry: Powdery mildew, Healthy
- Corn: Cercospora leaf spot, Common rust, Northern Leaf Blight, Healthy
- Grape: Black rot, Esca (Black Measles), Leaf blight, Healthy
- Orange: Huanglongbing (Citrus greening)
- Peach: Bacterial spot, Healthy
- Pepper bell: Bacterial spot, Healthy
- Potato: Early blight, Late blight, Healthy
- Raspberry: Healthy
- Soybean: Healthy
- Squash: Powdery mildew
- Strawberry: Leaf scorch, Healthy
- Tomato: Bacterial spot, Early blight, Late blight, Leaf mold, Septoria leaf spot, Spider mites, Target spot, Tomato Yellow Leaf Curl Virus, Tomato mosaic virus, Healthy

## Care Tips

The app provides care tips for each disease to help users manage and treat affected plants effectively.

## License

This project is licensed under the MIT License.

## Contact

For any questions or feedback, feel free to reach out:

Author: Nishant Kumar
GitHub: [github.com/Nishantr846](https://github.com/Nishantr846)