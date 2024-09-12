from flask import Flask, request, jsonify
import os
from datetime import datetime
from flask_cors import CORS
import face_recognition
import numpy as np

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
KNOWN_FACES_FOLDER = 'labled_images\\user'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(KNOWN_FACES_FOLDER):
    os.makedirs(KNOWN_FACES_FOLDER)

# Load known faces
known_face_encodings = []
known_face_names = []

for filename in os.listdir(KNOWN_FACES_FOLDER):
    if filename.endswith((".jpg", ".jpeg", ".png")):
        image = face_recognition.load_image_file(os.path.join(KNOWN_FACES_FOLDER, filename))
        encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(encoding)
        known_face_names.append(os.path.splitext(filename)[0])

@app.route('/upload-image', methods=['POST'])
def upload_image():
    print("Received upload request")
    if 'image' not in request.files:
        print("No file part")
        return jsonify({'error': 'No file part'}), 400

    file = request.files['image']
    if file.filename == '':
        print("No file selected")
        return jsonify({'error': 'No file selected'}), 400

    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    try:
        file.save(file_path)
        print(f"File saved: {file_path}")

        # Load the uploaded image
        unknown_image = face_recognition.load_image_file(file_path)

        # Find all the faces and face encodings in the unknown image
        face_locations = face_recognition.face_locations(unknown_image)
        face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

        face_names = []
        match_found = False
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                match_found = True

            face_names.append(name)
        old_file_name_index = filename.find('.')
        old_file_name = filename[:old_file_name_index]
        new_file_name = old_file_name + f'_{face_names[0]}.png'
        os.rename(f'uploads\\{filename}', f'uploads\\{new_file_name}')
        return jsonify({
            'success': True, 
            'filename': new_file_name, 
            'faces_detected': len(face_names),
            'recognized_faces': face_names,
            'match_found': match_found
        }), 200
        
    except Exception as e:
        print(f"Error processing file: {e}")
        return jsonify({'error': 'File processing failed'}), 500

if __name__ == '__main__':
    app.run(debug=True)