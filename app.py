from flask import Flask,send_file
from upload_pdf_requests import upload_bp
from elasticsearch import Elasticsearch
import jsonpickle


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'Uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}
app.register_blueprint(upload_bp, url_prefix='/upload')  # يمكنك تحديد البادئة هنا
es = Elasticsearch([
        {'host': '0c4f08cf97b74583acaddca9acbe9600.us-central1.gcp.cloud.es.io', 'port': 9243, "scheme": "https"}
    ],basic_auth=('elastic', 'Qbu6pDBxqb9ftwpgMYC0EOl8'))
@app.route('/', methods=['GET', 'POST'])
def index():
    return 'Hello World!'

@app.get('/search/<name>')
def search(name):
    search = es.search(index='students', body= {"query": {
        "match": {
            "name": str(name) 
        }}
    })
    return jsonpickle.encode(search['hits'], unpicklable=False)

@app.route('/download/<name>')
def download(name):
    
    return send_file('/Uploads/{name}', as_attachment=True)
    



if __name__ == '__main__':
    app.run(host='192.168.100.166',debug=False)
