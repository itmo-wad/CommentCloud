import logging
import os
import socket

from .. import app
from faker import Faker
from flask import Blueprint, send_from_directory, render_template
from flask import make_response
from flask_login import current_user
from flask_login import login_required

from . import auth
from . import fake_api

fake = Faker()

main = Blueprint('main', __name__)
logger = logging.getLogger(__name__)


@main.route('/', methods=['GET'])
def index():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    logger.info(str(IPAddr))
    return render_template('index.html')


@main.route('/admin', methods=['GET'])
@login_required
def admin():
    logger.info(str(current_user))
    return render_template('admin.html')


@main.route('/list_comment', methods=['GET'])
@login_required
def list_comment():
    # TODO
    # Add filter to get comments per siteadmin
    comments = fake_api.comment_database
    return render_template('list_comment.html', comments=comments)


@main.route('/generate_key', methods=['GET'])
@login_required
def generate_key():
    return render_template('generate_key.html')


@main.route('/gen_token', methods=['GET'])
@login_required
def gen_token():
    token = auth.get_token()
    return token


@main.route('/js/<string:script>')
def rout_js(script):
    return send_from_directory(os.path.join(app.root_path, 'static', 'js'),
                               script)

@main.route('/css/<string:style>')
def rout_css(style):
    return send_from_directory(os.path.join(app.root_path, 'static', 'css'),
                               style)

@main.route('/img/<string:img>')
def rout_img(img):
    return send_from_directory(os.path.join(app.root_path, 'static', 'img'),
                               img)

# Error handling 404
@app.errorhandler(404)
def not_found(error):
    """Page not found."""
    return make_response(render_template("error/404.html"), 404)


# Error handling 405
@app.errorhandler(405)
def bad_type(error):
    """Bad Type."""
    return make_response(render_template("error/405.html"), 405)


# Error handling 400
@app.errorhandler(400)
def bad_request():
    """Bad request."""
    return make_response(render_template("error/400.html"), 400)


# Error handling 500
@app.errorhandler(500)
def server_error():
    """Internal server error."""
    return make_response(render_template("error/500.html"), 500)