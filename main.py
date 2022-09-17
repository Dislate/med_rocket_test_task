import utils

if __name__ == '__main__':
    # Получение всех пользователей и задач
    all_users, all_tasks = utils.get_users_and_tasks("https://json.medrocket.ru/users",
                                                     "https://json.medrocket.ru/todos")
    # Создание директорий с отчетами
    utils.create_dir_if_not_exist("tasks")

    for user in all_users:
        # Проверка папки пользователя с отчетами
        user_path = f"tasks/{user['name']}"
        utils.create_dir_if_not_exist(user_path)
        # Список задач пользователя
        # Оптимизация за счет удаления из списка уже отобранных задач, уменьшая тем самым количество итераций
        user_tasks = [all_tasks.pop(i) for i in range(len(all_tasks))[::-1] if all_tasks[i]["userId"] == user["id"]]
        completed_tasks = [task for task in user_tasks if task["completed"]]
        exp_tasks = [task for task in user_tasks if not task["completed"]]

        report = utils.generate_report(user, completed_tasks, exp_tasks)
        utils.save_report(report, user_path, user["name"])
