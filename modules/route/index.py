from flask import render_template, Blueprint, session

index_route = Blueprint('index_route', __name__, template_folder='templates')


@index_route.route('/', methods=['GET'])
def defaultHtml():
    return render_template('index.html')


@index_route.route('/index.html', methods=['GET'])
def indexHtml():
    return render_template('index.html')
