# --coding  = utf-8
'''
单文件和文件夹上传
'''
from flask import Flask, abort, render_template, request, redirect, url_for
# from werkzeug import secure_filename
import os

app = Flask(__name__)
UPLOAD_FOLDER = './static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return redirect(url_for('hello'))  # 跳转到其他路由下


# 多路由公用一个
@app.route('/hello/')
@app.route('/hello/<name>')  # 传参
def hello(name=None):
    n = name
    print(type(name))
    print('n', n)
    return '''
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>带参URL传值方法</title>
</head>
<body>
    <h2>name</h2>
    <a href="{{ url_for('test',name=1) }}">点击这里查看</a>
</body>
</html>'''


# 测试文件夹上传、保存图片
@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist("file_folder")
        print('files', files)
        # 上传文件夹
        if len(files) > 1:
            for file in files:
                # print('file.filename:', file.filename)

                f_name = file.filename.split('/', -1)[1]
                # 判断保存文件夹是否存在
                if not os.path.exists(UPLOAD_FOLDER):
                    os.mkdir(UPLOAD_FOLDER)
                # 保存
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name))
            return "文件夹上传成功"
        # 上传单文件
        else:
            file = request.files['file']
            # filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'src.jpg'))
            return "单文件上传成功"
        # 测试代码
        # if files:
        #     for file in files:
        #         i = 0
        #         for i in range(len(request.files.getlist("file"))):
        #             filename = request.files.getlist("file")[i].filename.split('/', -1)[1]
        #             request.files.getlist("file")[i].save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #         i += 1
        #         return "upload success"
        #     return "上传成功"
    return '''<!doctype html>
<title>Upload new File</title>
<h1>Upload new File</h1>
<form method="POST" enctype=multipart/form-data>
  <p>文件夹: <input type='file' name="file_folder" webkitdirectory /></p>
  <p>单文件: <input type='file' name="file" /></p>
  
  <button>upload</button>
</form>
    '''


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port='5000', debug=True)
    app.run(host='0.0.0.0', port='5000')