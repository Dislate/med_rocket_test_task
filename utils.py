import os
import time
import requests
from datetime import datetime


def get_users_and_tasks(url_users: str, url_tasks: str) -> tuple:
    try:
        all_users = requests.get(url_users).json()
        all_tasks = [task for task in requests.get(url_tasks).json() if
                     len(task) == 4]  # Последние три записи не валидны, так как имеют один ключ 'id'
        return all_users, all_tasks
    except requests.exceptions.ConnectionError:
        print("Проверьте свое интернет соединение.\n"
              "Повторная попытка получить данные произойдет через 5 секунд\n"
              "-----------------------------------")
        time.sleep(5)
        return get_users_and_tasks(url_users, url_tasks)


def create_dir_if_not_exist(path: str = "") -> None:
    if not os.path.isdir(path):
        os.mkdir(path)


def generate_report(user: dict, comp_tasks: list[dict], exp_tasks: list[dict]) -> str:
    # Получение даты на момент создания отчета
    time_now = datetime.now()
    company, username, email = user["company"]["name"], user["name"], user["email"]
    # Шапка отчета
    header_report = f'''Отчёт для {company}.
{username} <{email}> {time_now.day:02d}.{time_now.month:02d}.{time_now.year} {time_now.hour:02d}:{time_now.minute:02d}
Всего задач: {len(comp_tasks) + len(exp_tasks)}\n\n'''
    # Завершенные задачи отчета
    comp_report = f'Завершенные задачи ({len(comp_tasks)}):\n'
    for comp_task in comp_tasks:
        comp_report += name_task(comp_task)
    comp_report += '\n'
    # Оставшиеся задачи отчета
    exp_report = f'Оставшиеся задачи ({len(exp_tasks)}):\n'
    for exp_task in exp_tasks:
        exp_report += name_task(exp_task)

    return header_report + comp_report + exp_report


def name_task(task: dict) -> str:
    if len(task["title"]) > 48:
        return f'{task["title"][:48]}...\n'
    return f'{task["title"]}\n'


def check_exist_report(report_path: str) -> bool:
    if os.path.isfile(report_path):
        return True
    return False


def save_report(report: str, user_path: str, user_name: str) -> None:
    file_name = '_'.join(user_name.split(' '))
    if check_exist_report(f'{user_path}/{file_name}.txt'):
        rename_old_report(user_path, file_name)
    with open(f"{user_path}/{file_name}.txt", "w") as f:
        f.write(report)
        f.close()


def rename_old_report(user_path: str, file_name: str) -> None:
    # Получение даты создания отчета
    c_time_report = os.path.getctime(f'{user_path}/{file_name}.txt')
    # Получение нормальной даты создания отчета
    n_time = datetime.fromtimestamp(c_time_report)
    # Генерация имени старого отчета
    old_report_name = f'old_{file_name}_{n_time.year}-{n_time.month:02d}-{n_time.day:02d}T{n_time.hour:02d}:' \
                      f'{n_time.minute:02d}.txt'
    # Переименовывание старого отчета
    os.rename(f"{user_path}/{file_name}.txt", f"{user_path}/{old_report_name}")
