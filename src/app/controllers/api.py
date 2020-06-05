import json
import logging
import re

import requests as request_other
from flask import Blueprint, request
from flask_login import current_user

from .auth import token_required
from .. import services

api = Blueprint('api', __name__)
logger = logging.getLogger(__name__)


@api.route('/test.add', methods=['GET'])
def add_comment_get():
    token = services.get_token_by_admin_email(current_user.id)
    token_value = token.TokenValue
    logger.info(token.TokenValue)
    logger.info(current_user.id)
    data = {"username": "Ledfgdrxi", "comment_object_id": "dfgsfv", "comment_text": "wevdfvdffwe"}
    data_json = json.dumps(data)
    newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = request_other.post("http://192.168.48.2/add.comment?token={token_value}".format(token_value=token_value), json=data_json, headers=newHeaders)
    logger.info(str(r))
    return "Okey"


@api.route('/add.comment', methods=['POST'])
@token_required
def add_comment():
    logger.info(str(request.content_type) + ",  " + str(request))
    if request.is_json:
        json_str = request.get_json()
        json_dict = json.loads(json_str)
        logger.info(str(request.args.get('token')))
        logger.info(str(type(json_dict)) + "  " + str(json_dict))
        if (("username" and "comment_object_id" and "comment_text") in json_dict) and len(json_dict) == 3:
            username = str(json_dict['username'])
            comment_object_id = str(json_dict['comment_object_id'])
            comment_text = str(json_dict['comment_text'])
            logger.info('func --add_comment: {u, id, text} - ' + username + ", " + comment_object_id + ", " + comment_text)
            if check_username(json_dict['username']) and check_comment_object_id(json_dict['comment_object_id']) and \
                    check_comment_text(json_dict['comment_text']):
                try:
                    token = request.args.get('token')
                    push_comment(token, username, comment_object_id, comment_text)
                except Exception as ex:
                    pass
            return "okey"
        else:
            return "Not okey"
    return "Redirected"


@api.route('/get.comments', methods=['POST'])
@token_required
def get_comments():



def push_comment(token, username, comment_object_id, comment_text):
    site_admin_id = services.get_site_admin_id_by_token_value(token)
    logger.info(site_admin_id)
    if site_admin_id is not None:
        services.add_comment(username=username, comment_object_id=comment_object_id,
                             comment_text=comment_text, site_admin_id=site_admin_id)
        logger.info(str(services.show_comments()))
        return "True"


def check_username(username):
    username = str(username)
    pattern = '^\w{1,16}$'
    if re.fullmatch(pattern, username) is not None:
        return username
    else:
        return None


def check_comment_object_id(comment_object_id):
    comment_object_id = str(comment_object_id)
    pattern = '^\w{1,32}$'
    if re.fullmatch(pattern, comment_object_id) is not None:
        return comment_object_id
    else:
        return None


def check_comment_text(comment_text):
    comment_text = str(comment_text)
    pattern = '^\w{1,64}$'
    if re.fullmatch(pattern, comment_text) is not None:
        return comment_text
    else:
        return None


# def check_token(token):
#     token = str(token)
#     pattern = "^\w{1,256}$"
#     if re.fullmatch(pattern, token) is not None:
#         return token
#     else:
#         return None
