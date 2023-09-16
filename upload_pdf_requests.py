import os
from flask import Blueprint, request, redirect, url_for, render_template, current_app
from werkzeug.utils import secure_filename
import uuid
import PyPDF2
from elasticsearch import Elasticsearch
from utils.filter import extractStudentInfo, textFilterToArray
es = Elasticsearch([
    {'host': '127.0.0.1', 'port': 9200, "scheme": "http"}
], verify_certs=False)

upload_bp = Blueprint('upload', __name__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@upload_bp.route('/')
def index():

    return 'Hello World!'


@upload_bp.route('/pdf', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        print('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = str(uuid.uuid4()) + '.' + \
            file.filename.rsplit('.', 1)[1].lower()
        upload_folder = os.path.join(
            current_app.root_path, current_app.config['UPLOAD_FOLDER'])

        file.save(os.path.join(upload_folder, filename))
        with open('./Uploads/' + filename, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            extracted_text = ''
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                extracted_text += page_text
            array = textFilterToArray(extracted_text)
            for item in array:
                extractStudentInfo(item, filename)
                # es.index(index='student',body=extractStudentInfo(item,filename))
            return {'message': 'File uploaded successfully'}, 200

    return {'message': 'Invalid file type'}, 400
