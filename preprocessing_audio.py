import os
from pydub import AudioSegment

UPLOAD_FOLDER = './static/UPLOADS'


def preprocess(filename):
    audio_file_path = 'static/UPLOADS/'+filename
    filename, file_extension = os.path.splitext(audio_file_path)
    if file_extension == '.mp3':
        return mp3_to_wav(audio_file_path,filename)
    else:
        return audio_file_path


def mp3_to_wav(audio_file_path, filename):
    sound = AudioSegment.from_mp3(audio_file_path)
    audio_file_path = filename.split('.')[0] + '.wav'
    sound.export(audio_file_path, format="wav")
    return audio_file_path
