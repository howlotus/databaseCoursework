from flask import Blueprint, render_template, current_app, request, session
from DB.sql_provider import SQLProvider
from DB.database import work_with_db

from access import group_permission_decorator

query_app = Blueprint('query', __name__, template_folder='templates')
provider = SQLProvider('scenario_query/sql/')


"""Шаблонная функция для каждого обработчика запроса. Принимает POST-параметры со страницы, проверяет их на пустоту и 
выполняет sql-запрос с выводом результатов на итоговую страницу"""


def func(file, rus_keys, string_value):
    value1 = request.form.get("value1", "")
    value2 = request.form.get('value2', "")
    if value1 != "" and value2 != "":
        sql = provider.get(file, sql_val1=value1, sql_val2=value2)
        result = work_with_db(current_app.config['DB_CONFIG'], sql)

        if not result:
            result_list = ['Таких записей нет.']
            eng_keys = 0
        else:
            result_list = result
            eng_keys = result[0].keys()
    else:
        result_list = ['Пустой ввод.']
        eng_keys = 0

    context = {'item_list': result_list, 'eng_keys': eng_keys, 'rus_keys': rus_keys, 'string_value': string_value,
               'profile': session.get('group_name', 'unauthorized')}
    return render_template('query_output.html', **context)


"""Обработчик выдачи страницы с меню запросов"""


@query_app.route('/')
@group_permission_decorator
def query_menu_handler():
    return render_template('query_choice.html', profile=session.get('group_name', 'unauthorized'))


"""Обработчик первого запроса, передача текста запроса и ключей."""


@query_app.route('/sql1', methods=['GET', 'POST'])
@group_permission_decorator
def query_sql1_handler():
    string_value = "Отчёт о заказе блюд"
    if request.method == 'GET':
        return render_template('query.html', string_value=string_value,
                               profile=session.get('group_name', 'unauthorized'))
    else:
        rus_keys = ['Уникальный номер блюда', 'Название блюда',
                    'Общее количество заказов блюда', 'Общая выручка от заказов блюда']
        return func('sql1.sql', rus_keys, string_value)


"""Обработчик второго запроса, передача текста запроса и ключей."""


@query_app.route('/sql2', methods=['GET', 'POST'])
def query_sql2_handler():
    string_value = "Отчёт о работе официантов"
    if request.method == 'GET':
        return render_template('query.html', string_value=string_value,
                               profile=session.get('group_name', 'unauthorized'))
    else:
        rus_keys = ['Уникальный номер официанта', 'Фамилия официанта', 'Общее количество принятых заказов',
                    'Общая сумма принятых заказов']
        return func('sql2.sql', rus_keys, string_value)


"""Обработчик третьго запроса, передача текста запроса и ключей."""


@query_app.route('/sql3', methods=['GET', 'POST'])
def query_sql3_handler():
    string_value = 'Показать сведения об официантах, ' \
             'не принявших ни одного заказа'
    if request.method == 'GET':
        return render_template('query.html', string_value=string_value,
                               profile=session.get('group_name', 'unauthorized'))
    else:
        rus_keys = ['Уникальный номер официанта', 'Фамилия официанта', 'Дата рождения',
                    'Адрес', 'Дата приёма на работу', 'Дата увольнения']
        return func('sql3.sql', rus_keys, string_value)
