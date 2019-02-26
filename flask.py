from flask import Flask, render_template, request
from load_prediction import predict
import os
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from werkzeug.utils import secure_filename
import os
import cv2

from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['PIC_FOLDER'] = './'
@app.route('/')

def index():
    return render_template('base.html')


@app.route('/picture', methods=['GET', 'POST'])
def get_data():
    if request.method == 'GET':
        try:
            pic = pickphoto()
            print(pic)
        except Exception as e:
            message = '数据采集失败:' + str(e)
        else:
            message = '数据采集成功'
            return render_template('picture.html')
    else:
        result = predict()
        print(result)
        return render_template('picture.html', result=result)





@app.route('/up_photo', methods=['post'])
def up_photo():
    img = request.files.get('photo')
    path = basedir + "/static/photo/"
    file_path = path + img.filename
    img.save(file_path)
    return render_template('picture.html')
# 设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)
@app.route('/hello')
def hello():
    return render_template('upload.html')

# @app.route('/upload', methods=['POST', 'GET'])
@app.route('/upload', methods=['POST', 'GET'])  # 添加路由
def upload():
    if request.method == 'POST':
        f = request.files['file']

        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})

        user_input = request.form.get("name")

        basepath = os.path.dirname(__file__)  # 当前文件所在路径

        upload_path = os.path.join(basepath, 'static/images/test', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        # upload_path = os.path.join(basepath, 'static/images','test.jpg')  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)

        # 使用Opencv转换一下图片格式和名称
        img = cv2.imread(upload_path)
        cv2.imwrite(os.path.join(basepath, 'static/images', 'test.jpg'), img)

        return render_template('picture.html', userinput=user_input)

    return render_template('picture.html')

# @app.route('/video')
# def video():

if __name__ == '__main__':
    app.run(debug=True)