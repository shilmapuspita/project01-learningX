import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

connection_string = 'mongodb+srv://shilmapuspita:Shilma17!@cluster0.luuvj.mongodb.net/'
client = MongoClient(connection_string)
db = client.dbsparta

MONGODB_URI = os.environ.get("mongodb+srv://shilmapuspita:Shilma17!@cluster0.luuvj.mongodb.net/")
DB_NAME =  os.environ.get("dbsparta")

client = MongoClient('mongodb+srv://shilmapuspita:Shilma17!@cluster0.luuvj.mongodb.net/')

db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({}, {'_id': False}))  # Mengambil data dari MongoDB
    return jsonify({'articles': articles})  # Mengirimkan data sebagai JSON

@app.route('/diary', methods=['POST'])
def save_diary():
        # Mengambil data dari form
        title_receive = request.form.get('title_give')
        content_receive = request.form.get('content_give')

        # Cek apakah file diterima
        file = request.files.get("file_give")
        if file is None:
            return jsonify({'message': 'File tidak ditemukan!'}), 400
        
        today = datetime.now()
        mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

        # Tentukan path dan nama file untuk disimpan
        extension = file.filename.split('.')[-1]
        filename = f'static/post-{mytime}.{extension}'


        # Simpan file di folder 'static'
        file.save(filename)

        profile = request.files['profile_give'] #menerima data dari client
        extension = profile.filename.split('.')[-1]
        profilename = f'static/profile-{mytime}.{extension}'

        # Simpan file di folder 'static'
        profile.save(profilename)


        # Menyusun dokumen untuk disimpan
        doc = {
            'file': filename,
            'profile': profilename,
            'title': title_receive,
            'content': content_receive
        }

        # Menyimpan dokumen ke MongoDB
        db.diary.insert_one(doc)

        # Mengembalikan respons sukses
        return jsonify({'message': 'data tersimpan!!!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)