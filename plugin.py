# -*- coding: utf-8 -*-
#########################################################
# python
import os, traceback

# third-party
import requests
from flask import Blueprint, request, send_file, redirect

# sjva 공용
from framework import app, path_data, check_api, py_urllib, SystemModelSetting, login_required
from framework.logger import get_logger
from framework.util import Util
from plugin import get_model_setting, Logic, default_route
from tool_base import ToolUtil
# 패키지
#########################################################

class P(object):
    package_name = __name__.split('.')[0]
    logger = get_logger(package_name)
    blueprint = Blueprint(package_name, package_name, url_prefix=f"/{package_name}", template_folder=os.path.join(os.path.dirname(__file__), 'templates'), static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    
    plugin_info = {
        'version' : '1.0.0',
        'name' : package_name,
        'category' : 'system',
        'icon' : '',
        'developer' : u'soju6jan',
        'description' : u'flaskcode fork',
        'home' : f'https://github.com/soju6jan/{package_name}',
        'more' : '',
    }
    menu = {}  

    ModelSetting = None
    logic = None
    module_list = None
    home_module = 'basic'


def initialize():
    try:
        P.module_list = []
        P.logic = Logic(P)
        ToolUtil.save_dict(P.plugin_info, os.path.join(os.path.dirname(__file__), 'info.json'))
    except Exception as e: 
        P.logger.error(f'Exception:{e}')
        P.logger.error(traceback.format_exc())


initialize()

