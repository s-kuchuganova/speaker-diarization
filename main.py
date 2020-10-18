import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from resemblyzer import VoiceEncoder, preprocess_wav
from pathlib import Path
import preprocessing_audio, model


UPLOAD_FOLDER = './static/UPLOADS'
ALLOWED_EXTENSIONS = {'wav', 'mp3'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('diarization',
                                    filename=filename))
    return '''
       <!doctype html>
       <title>Upload new File</title>
       <h1>Upload new File</h1>
       <form method=post enctype=multipart/form-data>
         <input type=file name=file>
         <input type=submit value=Upload>
       </form>
       '''


@app.route('/UPLOADS/<path:filename>')
def diarization(filename):
    wav_audio_path = preprocessing_audio.preprocess(filename)
    wav_fpath = Path(wav_audio_path)
    wav = preprocess_wav(wav_fpath)# VAD
    res = model.clustering(wav)
    return str(res)




