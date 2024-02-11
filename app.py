from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from your_python_script import process_image  # Import your processing script

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            result = process_image(file_path)  # Process the uploaded image
            return redirect(url_for('result', result=result))

@app.route('/result')
def result():
    video_paths = request.args.getlist('video_paths[]')
    return render_template('result.html', video_paths=video_paths)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
