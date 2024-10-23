from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import pandas as pd
import os
import shutil
from pathlib import Path
from script import process_csv_file  # Import your existing logic from the script

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'

# Ensure directories exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
if not os.path.exists(app.config['OUTPUT_FOLDER']):
    os.makedirs(app.config['OUTPUT_FOLDER'])

# Home route to display the file upload form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the file upload and process it
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file.filename != '':
        return render_template('header.html') 
    
    # Save the file to the uploads folder
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Call the process_csv_file function (your script logic)
    try:
        result_file = process_csv_file(file_path, app.config['OUTPUT_FOLDER'])
    except Exception as e:
        return str(e)

    # After processing, redirect to download the zip
    return redirect(url_for('download_file', filename=result_file))

# Route to download the processed file
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
