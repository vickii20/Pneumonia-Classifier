from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os
import tempfile

# Constants
MODEL_PATH = 'lung_disease_detection_model.h5'
IMAGE_SIZE = (150, 150)  # Ensure this matches the model's input size
CLASS_NAMES = ['Normal', 'Pneumonia']  # Update based on your model's classes

# Load the trained model
model = load_model(MODEL_PATH)

# Initialize Flask app
app = Flask(__name__, template_folder='frontend', static_folder='frontend')

# Ensure temp_uploads directory exists
UPLOAD_FOLDER = 'temp_uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

# Define the route for image prediction
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400

    try:
        # Create a temporary file to store the uploaded image
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            file.save(tmp_file.name)
            tmp_file.seek(0)
            
            # Load and preprocess the image
            img = load_img(tmp_file.name, target_size=IMAGE_SIZE)
            img_array = img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = img_array / 255.0  # Normalize if the model was trained with normalization

            # Perform the prediction
            prediction = model.predict(img_array)

            # Handle multi-class output (e.g., softmax) and get the predicted class
            predicted_index = np.argmax(prediction[0])
            predicted_class = CLASS_NAMES[predicted_index]

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        os.remove(tmp_file.name)  # Clean up temporary file

    return jsonify({'prediction': predicted_class})

def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# Run the Flask server
if __name__ == '__main__':
    app.run(debug=True)
