from flask import Flask,send_file
from upload_pdf_requests import upload_bp
from elasticsearch import Elasticsearch
import jsonpickle


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'Uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}
app.register_blueprint(upload_bp, url_prefix='/upload')  # يمكنك تحديد البادئة هنا
es = Elasticsearch([
        {'host': '127.0.0.1', 'port': 9200, "scheme": "https"}
    ], verify_certs=False)
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
    app.run(host='0.0.0.0',debug=False)
