# U-Net发型分割及染发


训练好的模型:src/weights.002.h5或src/weights.005.h5

运行web端服务:python3 web_api_hair_recolor.py

打开浏览器:
http://127.0.0.1:5000/hair_recolor/upload
http://127.0.0.1:5000/hair_recolor/upload/银色
http://127.0.0.1:5000/hair_recolor/upload/20,30,60  

> 注：20,30,60为对应RGB值
> 可以使用中文参数设置
> 默认颜色某种紫色RGB(102, 22, 64)

<img src="screenshots/测试截图.png" alt="测试" style="zoom: 80%;" />
