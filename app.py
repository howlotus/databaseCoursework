from flask import Flask, render_template, session
from scenario_query.routes import query_app
from scenario_auth.routes import auth_app
from scenario_order.routes import order_app

import json

from access import group_permission_decorator

app = Flask(__name__)
app.register_blueprint(query_app, url_prefix='/query')
app.register_blueprint(auth_app, url_prefix='/auth')
app.register_blueprint(order_app, url_prefix='/order')

app.config['DB_CONFIG'] = json.load(open('configs/db.json', 'r'))
app.config['ACCESS_CONFIG'] = json.load(open('configs/access.json', 'r'))
app.config['SECRET_KEY'] = 'my super secret key'


"""Обработчик выдачи пользователю главного меню"""


@app.route('/')
@group_permission_decorator
def main_menu_handler():
    return render_template('main_menu.html', profile=session.get('group_name', 'unauthorized'))


"""Завершение работы. Очищение всей сессии."""


@app.route('/exit')
@group_permission_decorator
def exit_page_handler():
    session.clear()
    return render_template('work_interruption.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5011)
