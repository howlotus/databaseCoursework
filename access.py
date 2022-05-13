from functools import wraps
from flask import session, current_app, request, render_template


"""Функция проверки текущего пользователя на наличие доступа к обработчику. Сначала проверяется доступ к модулю в целом,
затем отдельно проверяется обработчик, если доступа к модулю не найдено или попытка получить доступ происходит не к
модулю"""


def is_group_permission_valid():
    config = current_app.config['ACCESS_CONFIG']
    group_name = session.get('group_name', 'unauthorized')

    t = request.endpoint.split('.')

    for i in t:
        target_app = i
        if group_name in config and target_app in config[group_name]:
            return True, group_name

    return False, group_name


"""Декоратор для проверки пользователя на предмет авторизованности"""


def group_permission_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        a, group_name = is_group_permission_valid()
        if a:
            return f(*args, **kwargs)
        return render_template('permission_denied.html', profile=group_name)
    return wrapper
