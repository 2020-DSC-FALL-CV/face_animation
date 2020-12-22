from flask import Flask, render_template, request, redirect
from flask_dropzone import Dropzone
import os
import sys
import shutil
from werkzeug.datastructures import ImmutableMultiDict
basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(basedir,"..","Face2Cartoon","test"))
from cartoonize import Model


load_folder = os.path.join(basedir,"static","images","uploads")
save_folder = os.path.join(basedir,"..","Face2Cartoon","cartoonized_images")
upload_dir = os.path.join(basedir, "static","images","uploads")
app = Flask(__name__)
app.config['UPLOADED_PATH'] = upload_dir


""" Dropzone Configuration """
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image'
app.config['DROPZONE_MAX_FILES'] = 1
app.config['DROPZONE_IN_FORM'] = True
app.config['DROPZONE_UPLOAD_ON_CLICK'] = True
app.config['DROPZONE_UPLOAD_ACTION'] = 'ask'
app.config['DROPZONE_UPLOAD_BTN_ID'] = 'submit'
app.config['DROPZONE_DEFAULT_MESSAGE'] = '사진 업로드: 클릭하거나 파일을 드래그해주세요.'
app.config['DROPZONE_MAX_FILE_SIZE'] = 10
##################################################################
dropzone = Dropzone(app)
cartoonize=Model()
global tempfname, id 
@app.route('/')
def mainpage():
    return render_template('index.html')

global tempfname
tempfname = ''


""" 사용자 요청 페이지 """
@app.route('/Face2Cartoon_q', methods=['GET', 'POST'])
def ask():

    # 사용자 요청 발생 시
    global tempfname, id
    if request.method == 'POST':
        """ 파일 저장 """
        if request.files != ImmutableMultiDict([]):
            for key, f in request.files.items():
                if key.startswith('file'):
                    tempfname = f.filename
                    print(tempfname)
                    id = tempfname.split(".")[0]
                    print(id)

                    if os.path.exists(app.config['UPLOADED_PATH']):
                        shutil.rmtree(app.config['UPLOADED_PATH'])
                    if not os.path.exists(app.config['UPLOADED_PATH']):
                        os.mkdir(app.config['UPLOADED_PATH'])

                    f.save(os.path.join(app.config['UPLOADED_PATH'], tempfname))
            return '', 204

        else:
            # 결과 페이지로 이동
            return redirect('/Face2Cartoon_a?id='+str(id))
    # 기본 화면
    return render_template('Face2Cartoon_q.html')

""" 결과 페이지 """
@app.route('/Face2Cartoon_a', methods=['GET', 'POST'])
def answer():
    global tempfname
    if request.method == 'GET':
        page = request.args.get('page', type=int, default=1)
        file_list = os.listdir(app.config['UPLOADED_PATH'])
        print('1')
        print(app.config['UPLOADED_PATH'])
        print(file_list)
        cartoonize.main(load_folder, save_folder)

        cartoon_dir = os.path.join(basedir,"..","Face2Cartoon","cartoonized_images")
        cartoon_image= save_folder + '/' + tempfname
        print(tempfname)
        print('2')
        print(cartoon_image)

        output_dir = os.path.join(basedir,'static','output')
        output_name = tempfname
        shutil.move(cartoon_image,os.path.join(output_dir,output_name))
        asked = 'output' +'/'+ tempfname
        print(asked)
        return render_template('Face2Cartoon_a.html', asked = asked)



if __name__ == '__main__':
    app.run(host="0.0.0.0")
