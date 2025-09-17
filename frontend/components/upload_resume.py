from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['resume']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        file_path = os.path.join('data/resumes', file.filename)
        file.save(file_path)
        return jsonify({'message': 'Resume uploaded successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)