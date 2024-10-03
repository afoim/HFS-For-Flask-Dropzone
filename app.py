from flask import Flask, render_template, request, send_from_directory
from flask_dropzone import Dropzone
import os

app = Flask(__name__)
dropzone = Dropzone(app)

# 设置文件上传目录
app.config['DROPZONE_UPLOAD_MULTIPLE'] = False
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'file'
app.config['DROPZONE_MAX_FILE_SIZE'] = 50  # 最大文件大小为50MB
UPLOAD_FOLDER = 'Files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)  # 获取已上传文件列表
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        if os.path.exists(file_path):
            return '文件已存在', 400  # 返回400错误
        file.save(file_path)
        return '文件上传成功', 200
    return '没有文件上传', 400

@app.route('/files/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=30001, debug=True)
