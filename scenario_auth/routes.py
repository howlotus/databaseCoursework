from flask import Blueprint, session, render_template, request, current_app
from DB.sql_provider import SQLProvider
from DB.database import work_with_db
from access import group_permission_decorator


auth_app = Blueprint('auth', __name__, template_folder='templates')
provider = SQLProvider('scenario_auth/sql/')

"""Авторизация. После получения данных со страницы гарантировано их наличие, соответственно, их проверки не требуется.
Если введённые данные есть в БД, то авторизация успешна и пользователь получает необходимые ему права, иначе
требуется вводить данные снова"""


@auth_app.route('/login', methods=['GET', 'POST'])
@group_permission_decorator
def login_page_handler():
    if request.method == 'GET':
        group_name = session.get('group_name', 'unauthorized')
        return render_template('authorization.html', profile=group_name)
    else:
        login = request.form.get('login')
        password = request.form.get('password')

        sql = provider.get('login_password.sql', sql_val1=login, sql_val2=password)
        result = work_with_db(current_app.config['DB_CONFIG'], sql)

        if not result:
            message = 'Введён неверный логин или пароль!'

            return render_template('login_message.html', string_value=[], message=message)
        else:
            message = 'Вход успешно выполнен!'
            session['group_name'] = result[0]['Permission_Value']
            if result[0]['Permission_Value'] == 'waiter' or result[0]['Permission_Value'] == 'admin':
                sql = provider.get('get_waiter_data.sql', sql_val=login)
                w_id_name = work_with_db(current_app.config['DB_CONFIG'], sql)
                if w_id_name:
                    session['waiter'] = w_id_name

            return render_template('login_message.html', string_value=login, message=message,
                                   profile=result[0]['Permission_Value'])
