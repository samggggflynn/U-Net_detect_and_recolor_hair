# coding:utf-8
'''
API: recolor_hair
Author: LXC
date: 2019年11月24日
'''
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, Response
import json
from werkzeug.utils import secure_filename
import os
import cv2
from datetime import timedelta
from src.demo import predict, change_v, recolor
import time
import keras


# 设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


app = Flask(__name__)
UPLOAD_FOLDER = './static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # 上传文件夹
app.config['JSON_AS_ASCII'] = False  # 设置json显示中文
# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)


@app.route('/hair_recolor/upload', methods=['POST', 'GET'])  # 添加路由
@app.route('/hair_recolor/upload/<string:color>', methods=['POST', 'GET'])  # 添加带颜色参数的路由
def upload(color=(0x40, 0x16, 0x66)):
    if request.method == 'POST':
        Colors = {
            '银色':     [169, 169, 169],
            '皇家蓝':   [65, 105,  225],
            '紫色':     [128, 0,   128],
            '浅粉':     [255, 182, 193],
            '深粉':     [255, 20,  147],
            '巧克力':	 [210, 105,  30],
            '森林绿':	 [34,  139,  34]}

        file = request.files['file']
        if not (file and allowed_file(file.filename)):
            return jsonify({"error": 1001, "error_msg": "format error：请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'src.jpg'))
        print("单文件上传成功")
        # model模型位置， ifn 原图， ofn 处理结果图， （考虑将color设置为含参数路由）
        ifn = os.path.join(app.config['UPLOAD_FOLDER'], 'src.jpg')
        ofn = 'static/res.jpg'
        src = cv2.imread(ifn)
        start = time.perf_counter()
        model = keras.models.load_model('weights.005.h5')
        mask = predict(model, src)
        keras.backend.clear_session()  # 清除session（否则keras报错）
        print(time.perf_counter() - start)
        start = time.perf_counter()
        # 设置颜色，判断颜色参数是RGB的十六进制还是颜色字典键值对
        if isinstance(color, str):
            try:
                # 直接RGB值取色
                co = []
                for rgb in color.split(','):
                    # print("rgb", rgb)
                    if rgb.startswith('0x'or'0X'):
                        co.append(int(rgb, 16))  # 将16进制str转为10进制int整数
                        if len(co) == 3:
                            co.reverse()
                    else:
                        co.append(int(rgb, 10))  # 将10进制str转为10进制int整数
                        if len(co) == 3:
                            co.reverse()
                # list转tuple
                color = tuple(co)
            except:
                # 字典键值对取色
                for key in Colors:
                    if color == key:
                        # print(Colors[color][::-1])
                        color = tuple(Colors[color][::-1])
        res = recolor(src, mask, color)
        print(time.perf_counter() - start)
        cv2.imwrite(ofn, res)

        return '''
        <!DOCTYPE html>

<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>XC's LAB</title>
    <link href="https://cdn.bootcss.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.bootcss.com/popper.js/1.12.9/umd/popper.min.js"></script>
    <script src="https://cdn.bootcss.com/jquery/3.3.1/jquery.min.js"></script>
    <script src="https://cdn.bootcss.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
    <!--    <link href="/static/css/main.css" rel="stylesheet">-->
</head>
<body>
<nav class="navbar navbar-expand-sm bg-dark navbar-dark">
    <!-- Brand/logo -->
    <!--      <a class="navbar-brand" href="#">Logo</a>-->
    <div class="container">
        <a class="navbar-brand" href="#">XC's LAB</a>
        <!-- Links -->
        <ul class="navbar-nav">
            <li class="nav-item">
                <a class="nav-link" href="https://baidu.com" target="_blank">百度</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="https://google.com" target="_blank">Google</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="enhance/upload">暗光增强</a>
            </li>
        </ul>
        <button class="btn btn-outline-secondary my-2 my-sm-0" href="github.com">Github</button>
    </div>
</nav>
<div class="container">
    <div id="content" style="margin-top:4em">
        <h2>更换发色</h2>
        <h3>（图像尽量清晰，支持url+RGB赋值，如，https//:.../hair_recolor/upload/102,22,64或https//:.../hair_recolor/upload/0x46,0x22,0x64）</h3>

        <form action="" enctype='multipart/form-data' method='POST'>
            <input type="file" name="file" style="margin-top:20px;"/>
            <br>

            <input type="submit" value="上传" class="button-new" style="margin-top:15px;"/>
        </form>
        <table>
            <tr>
                <td>

                    <a><img src="/static/src.jpg" alt="你的图片被外星人劫持了～～" width="600" height=auto ALIGN=left/></a>
                </td>
                <td>
                    <a><img src="/static/res.jpg" alt="你的图片被外星人劫持了～～" width="600" height=auto ALIGN=right/></a>
                </td>
            </tr>
        </table>

    </div>
</div>
</body>
</html>'''
    return '''
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>XC's LAB</title>
    <link href="https://cdn.bootcss.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.bootcss.com/popper.js/1.12.9/umd/popper.min.js"></script>
    <script src="https://cdn.bootcss.com/jquery/3.3.1/jquery.min.js"></script>
    <script src="https://cdn.bootcss.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
    <!--    <link href="/static/css/main.css" rel="stylesheet">-->
</head>
<body>
<nav class="navbar navbar-expand-sm bg-dark navbar-dark">
    <!-- Brand/logo -->
    <!--      <a class="navbar-brand" href="#">Logo</a>-->
    <div class="container">
        <a class="navbar-brand" href="#">XC's LAB</a>
        <!-- Links -->
        <ul class="navbar-nav">
            <li class="nav-item">
                <a class="nav-link" href="https://baidu.com" target="_blank">百度</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="https://google.com" target="_blank">Google</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="enhance/upload">暗光增强</a>
            </li>
        </ul>
        <button class="btn btn-outline-secondary my-2 my-sm-0" href="github.com">Github</button>
    </div>
</nav>
<div class="container">
    <div id="content" style="margin-top:4em">
        <h2>更换发色</h2>
        <h3>（图像尽量清晰，支持url+RGB赋值，如，https//:.../hair_recolor/upload/102,22,64或https//:.../hair_recolor/upload/0x46,0x22,0x64）</h3>
<form action="" enctype='multipart/form-data' method='POST'>
    <input type="file" name="file" style="margin-top:20px;"/>
    <br>

    <input type="submit" value="上传" class="button-new" style="margin-top:15px;"/>
</form>
</body>
</html>'''


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port='5000', debug=True)
    app.run(host='0.0.0.0', port='5000')
