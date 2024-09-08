from flask import Flask, flash, request, redirect, render_template 
from werkzeug.utils import secure_filename
import subprocess
import pickle 
import os
import ast
 
model = pickle.load (open ('Model/model.pkl', 'rb')) 

app = Flask(__name__)
app.secret_key = "secret key" 

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
path = os.getcwd()

UPLOAD_FOLDER = os.path.join(path, 'uploads')
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['csv'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route ('/') 
def index (): 
    return render_template ("index.html") 
 
 
@app.route ('/result', methods =['POST']) 
def result (): 
    file = request.files['eeg_file']

    if file.filename == '':
        flash('No file selected for uploading')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        custom_filename = "eegfile." + file_extension
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], custom_filename))
        flash("File successfully uploaded")
    else:
        return "Allowed file types are txt, pdf, png, jpg, jpeg, gif"
    
    filepath = r"D:/MAJOR PROJECT/uploads/eegfile.csv"
    # start the processing asynchronously using a subprocess to summarise the text
    process = subprocess.Popen(['python', 'D:/MAJOR PROJECT/prediction.py', filepath], stdout=subprocess.PIPE)

    # Wait for the process to finish and capture the output
    process.wait()

    output, error = process.communicate()
    if error:
        return "an error occured"
    
    output_str = output.decode('utf-8').strip()
    result_list = ast.literal_eval(output_str)

     # Extract result and confidence
    result = result_list[0]
    confidence = result_list[1]

    if(result == 0):
        result = 'Non-Parkinson'
    else:
        result = 'Parkinson'
    
    return render_template('result.html', result=result, confidence=confidence)
    

    
if __name__ == '__main__':
    app.run (debug = True) 