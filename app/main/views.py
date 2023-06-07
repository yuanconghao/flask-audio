from app import get_logger, get_config
import math
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import utils
from app.models import CfgNotify
from app.main.forms import CfgNotifyForm
from . import main
import os
import subprocess
import time
from datetime import datetime
import app.main.const as c
import zhconv
import requests
import json

logger = get_logger(__name__)
cfg = get_config()


# 通用列表查询
def common_list(DynamicModel, view):
    # 接收参数
    action = request.args.get('action')
    id = request.args.get('id')
    page = int(request.args.get('page')) if request.args.get('page') else 1
    length = int(request.args.get('length')) if request.args.get('length') else cfg.ITEMS_PER_PAGE

    # 删除操作
    if action == 'del' and id:
        try:
            DynamicModel.get(DynamicModel.id == id).delete_instance()
            flash('删除成功')
        except:
            flash('删除失败')

    # 查询列表
    query = DynamicModel.select()
    total_count = query.count()

    # 处理分页
    if page: query = query.paginate(page, length)

    dict = {'content': utils.query_to_list(query), 'total_count': total_count,
            'total_page': math.ceil(total_count / length), 'page': page, 'length': length}
    return render_template(view, form=dict, current_user=current_user)


# 通用单模型查询&新增&修改
def common_edit(DynamicModel, form, view):
    id = request.args.get('id', '')
    if id:
        # 查询
        model = DynamicModel.get(DynamicModel.id == id)
        if request.method == 'GET':
            utils.model_to_form(model, form)
        # 修改
        if request.method == 'POST':
            if form.validate_on_submit():
                utils.form_to_model(form, model)
                model.save()
                flash('修改成功')
            else:
                utils.flash_errors(form)
    else:
        # 新增
        if form.validate_on_submit():
            model = DynamicModel()
            utils.form_to_model(form, model)
            model.save()
            flash('保存成功')
        else:
            utils.flash_errors(form)
    return render_template(view, form=form, current_user=current_user)


def common_trans_zh(DynamicModel, form, view):
    return render_template(view, form=form, current_user=current_user)


# 根目录跳转
@main.route('/', methods=['GET'])
# @login_required
def root():
    return redirect(url_for('main.index'))


# 首页
@main.route('/index', methods=['GET'])
# @login_required
def index():
    return render_template('index.html')


# 通知方式查询
@main.route('/notifylist', methods=['GET', 'POST'])
# @login_required
def notifylist():
    return common_list(CfgNotify, 'notifylist.html')


# 通知方式配置
@main.route('/notifyedit', methods=['GET', 'POST'])
# @login_required
def notifyedit():
    return common_edit(CfgNotify, CfgNotifyForm(), 'notifyedit.html')


@main.route('/audio_trans_zh', methods=['GET', 'POST'])
# @login_required
def audio_trans_zh():
    return common_trans_zh(CfgNotify, CfgNotifyForm(), 'trans_zh.html')


@main.route('/hello')
# @login_required
def hello_world():
    return 'Hello World!1'


@main.route('/audio_upload', methods=['POST'])
# @login_required
def audio_upload():
    res = {
        'code': 0,
        'msg': '',
        'data': {}
    }
    # file_rename = request.form['rename'].strip()
    file_obj = request.files['file']
    print(file_obj)
    if file_obj is None:
        res['code'] = 1001
        res['msg'] = 'upload err, try again'
        return res

    file_name = file_obj.filename
    if file_name == '':
        res['code'] = 1002
        res['msg'] = 'upload file empty'
        return res

    file_suffix = os.path.splitext(file_name)[-1]

    suffix_types = ['.wav', '.mp3']
    if file_suffix not in suffix_types:
        res['code'] = 1003
        res['msg'] = 'upload file type err, only support wav/mp3'
        return res

    file_read = file_obj.read()
    file_size = len(file_read)
    max_file_size = 100 * 1000 * 1000
    if file_size > max_file_size:
        res['code'] = 1004
        res['msg'] = 'upload file size err, max size 100MB'
        return res

    # 20230523
    date_now = datetime.now().strftime("%Y%m%d")
    # timestamp
    time_now = int(time.time())
    # /data/audio-core/20230523/
    # file_s_name = str(time_now)
    # if file_rename != '':
    #     file_s_name = file_rename

    # upload_path = os.path.join(c.AUDIO_BASE_PATH, date_now) + '/'
    # relative_path = date_now + '/' + file_s_name + file_suffix
    relative_path = 'data/' + file_name
    upload_path = os.path.join(c.AUDIO_BASE_PATH, 'data/')
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)

    upload_file_path = upload_path + file_name
    with open(upload_file_path, 'wb+') as f:
        f.write(file_read)

    f.close()

    data = {
        'file_name': file_name,
        'path': relative_path
    }
    res['msg'] = "success"
    res['data'] = data
    return res


@main.route('/audio_translate', methods=['POST'])
def audio_translate():
    res = {
        'code': 0,
        'msg': '',
        'data': {}
    }

    file_r_path = str(request.form.get('path'))
    file_name = file_r_path.split('/')[-1]

    lang = request.form.get('lang')

    if file_r_path is None:
        res['code'] = 10001
        res['msg'] = 'path is empty'
        return res

    file_path = c.AUDIO_BASE_PATH + file_r_path
    if not os.path.exists(file_path):
        res['code'] = 10002
        res['msg'] = 'file is empty, please upload first'
        return res

    print(file_path)
    # ffmpeg
    cmd = f"ffmpeg -i {file_path} -vn -b:a 192k -ar 44100 -ac 2 -acodec libmp3lame -y {file_path}"
    print(cmd)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result)

    url = "https://api.openai.com/v1/audio/transcriptions"

    payload = {
        'model': 'whisper-1',
        'language': lang
    }
    files = [
        ('file', (file_name, open(file_path, 'rb'), 'audio/wav'))
    ]

    headers = {
        'Authorization': 'Bearer ' + c.OPENAI_API_KEY
    }

    print(headers)

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)
    text = json.loads(response.text)
    # if text['error']:
    #     res['code'] = 10003
    #     res['msg'] = text['error']['code']
    #     return res
    data = {
        "text": zhconv.convert(text['text'], 'zh-hans')
    }
    res['data'] = data
    return res


@main.route('/audio_translate_c', methods=['POST'])
def audio_translate_c():
    res = {
        'code': 0,
        'msg': '',
        'data': {}
    }
    file_r_path = request.form.get('path')
    model = request.form.get('model')
    lang = request.form.get('lang')

    if file_r_path is None:
        res['code'] = 10001
        res['msg'] = 'path is empty'
        return res

    file_path = c.AUDIO_BASE_PATH + file_r_path
    if not os.path.exists(file_path):
        res['code'] = 10002
        res['msg'] = 'file is empty, please upload first'
        return res

    print(file_path)
    if model is None:
        model = 'small'
    if model not in ['base', 'small', 'medium']:
        res['code'] = 10003
        res['msg'] = 'model must in base/small/medium'
        return res

    if lang is None:
        lang = 'zh'
    if lang not in c.WHISPER_LANG.keys():
        res['code'] = 10004
        res['msg'] = 'lang illegal'
        return res

    # /Users/conghaoyuan/cpp/whisper.cpp/main -m /Users/conghaoyuan/cpp/whisper.cpp/models/ggml-base.bin -l zh -t 2 -f /Users/conghaoyuan/data/audio-core/data/jfk.wav -otxt --prompt '简体中文'
    cmd = f"{c.WHISPER_PATH}main -m {c.WHISPER_MODEL_PATH}{c.WHISPER_MODEL_MAP[model]} -l {lang} -t 2 -p 2 -f {file_path} -otxt"
    if lang == 'zh':
        cmd += " --prompt '简体中文'"
    print(cmd)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    strout = result.stdout.splitlines()
    out_list = []
    for x in strout:
        if x == "":
            continue

        out_list.append(zhconv.convert(x, 'zh-hans'))
    # strout = [x for x in strout if x]

    data = {
        'path': file_r_path + '.txt',
        'strout': out_list,
    }
    res['msg'] = 'success'
    res['data'] = data
    return res
