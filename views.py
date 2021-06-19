# -*- coding: utf-8 -*-
import os
import mimetypes
from flask import render_template, abort, jsonify, send_file, g, request
from .utils import write_file, dir_tree, get_file_extension
from . import blueprint

from framework import app, path_data, check_api, py_urllib, SystemModelSetting, login_required

exclude_names=['mount', 'mnt', '__pycache__']
excluded_extensions=['mp4', 'db', 'pyo']


@blueprint.route('/')
@login_required
def index():
    dirname = os.path.basename(g.flaskcode_resource_basepath)
    dtree = dir_tree(g.flaskcode_resource_basepath, g.flaskcode_resource_basepath + '/', exclude_names=exclude_names, excluded_extensions=excluded_extensions, )
    return render_template('flaskcode/index.html', dirname=dirname, dtree=dtree, file_loading="")

@blueprint.route('/<path:path>')
@login_required
def index2(path):
    dirname = os.path.basename(g.flaskcode_resource_basepath)
    dtree = dir_tree(g.flaskcode_resource_basepath, g.flaskcode_resource_basepath + '/', exclude_names=exclude_names, excluded_extensions=excluded_extensions, )
    file_path = os.path.join(g.flaskcode_resource_basepath, path)
    if os.path.isfile(file_path):
        file_loading = path
    else:
        file_loading = ''
    return render_template('flaskcode/index.html', dirname=dirname, dtree=dtree, file_loading=file_loading)

@blueprint.route('/resource-data/<path:file_path>.txt', methods=['GET', 'HEAD'])
def resource_data(file_path):
    file_path = os.path.join(g.flaskcode_resource_basepath, file_path)
    if not (os.path.exists(file_path) and os.path.isfile(file_path)):
        abort(404)
    response = send_file(file_path, mimetype='text/plain', cache_timeout=0)
    mimetype, encoding = mimetypes.guess_type(file_path, False)
    if mimetype:
        response.headers.set('X-File-Mimetype', mimetype)
        extension = mimetypes.guess_extension(mimetype, False) or get_file_extension(file_path)
        if extension:
            response.headers.set('X-File-Extension', extension.lower().lstrip('.'))
    if encoding:
        response.headers.set('X-File-Encoding', encoding)
    return response


@blueprint.route('/update-resource-data/<path:file_path>', methods=['POST'])
def update_resource_data(file_path):
    file_path = os.path.join(g.flaskcode_resource_basepath, file_path)
    is_new_resource = bool(int(request.form.get('is_new_resource', 0)))
    if not is_new_resource and not (os.path.exists(file_path) and os.path.isfile(file_path)):
        abort(404)
    success = True
    message = 'File saved successfully'
    resource_data = request.form.get('resource_data', None)
    if resource_data:
        success, message = write_file(resource_data, file_path)
    else:
        success = False
        message = 'File data not uploaded'
    return jsonify({'success': success, 'message': message})