import datetime
import json
import operator


def interface():
    while True:
        print("\nГЛАВНОЕ МЕНЮ")
        command = input("Введите команду (add, list, find, exit): ").lower()
        if command == "add":
            interface_create_note()
            continue
        elif command == "list":
            list_notes()
            continue
        elif command == "find":
            view_note(find_notes())
            continue
        elif command == "exit":
            print("\nПрограмма завершена!")
            break
        else:
            print("Ошибка! Не найдена команда, повторите попытку!")


def interface_create_note():
    print("\nСОЗДАНИЕ НОВОЙ ЗАМЕТКИ")
    fields = dict()
    fields['id'] = int(max_id()) + 1
    fields['head'] = input("Заголовок заметки: ")
    fields['body'] = input("Тело заметки: ")
    fields['data_create'] = datetime.datetime.now().strftime("%d %B %Y %H:%M:%S")
    fields['data_edit'] = datetime.datetime.now().strftime("%d %B %Y %H:%M:%S")
    while True:
        print("\nВыберите действие:")
        print("1. Сохранить")
        print("2. Отменить")
        action = int(input("Введите номер: "))
        if action == 1:
            list_of_dicts.append(fields)
            save_db()
            print("\nЗаметка сохранена!")
            break
        elif action == 2:
            break
        else:
            print("Неверный пункт меню. Повторите попытку.")


def max_id():
    if len(list_of_dicts) == 0:
        return 0
    else:
        max = 0
        for i in range(len(list_of_dicts)):
            if list_of_dicts[i]['id'] > max:
                max = list_of_dicts[i]['id']
        return max


def save_db():
    list_of_dicts.sort(key=operator.itemgetter('data_edit'), reverse=True)
    json_str = json.dumps(list_of_dicts)
    with open(db, 'w') as file:
        file.write(json_str)


def open_db():
    with open(db, 'a') as file:
        file.write("")
    with open(db, 'r') as file:
        json_str = file.read()
    if json_str == "":
        return list()
    else:
        return json.loads(json_str)


def list_notes():
    print("\nСПИСОК ЗАМЕТОК")
    if len(list_of_dicts) == 0:
        print("Заметок нет")
        return
    else:
        for i in range(len(list_of_dicts)):
            for item in list_of_dicts[i]:
                print('{}: {}'.format(item, list_of_dicts[i][item]))
            print()
    actions_notes(0)


def actions_notes(id_out):
    while True:
        print("\nВыберите действие:")
        print("1. Редактировать")
        print("2. Удалить")
        print("3. Отменить")
        action = int(input("Введите номер: "))
        if (action == 1 or action == 2) and id_out == 0:
            id = int(input("Введите id заметки: "))
            for i in range(len(list_of_dicts)):
                if list_of_dicts[i]['id'] == id:
                    id_note = i
                    break
                if i + 1 == len(list_of_dicts):
                    print("\nЗаметка не найдена!")
                    action = 3
        else:
            id_note = id_out
        if action == 1:
            print("\nРЕДАКТИРОВАНИЕ ЗАМЕТКИ")
            print('#{}\t{}'.format(list_of_dicts[id_note]['id'], list_of_dicts[id_note]['data_edit']))
            print('{}: {}'.format('Заголовок', list_of_dicts[id_note]['head']))
            list_of_dicts[id_note]['head'] = input("Новый заголовок: ")
            print('{}: {}'.format('Тело заметки', list_of_dicts[id_note]['body']))
            list_of_dicts[id_note]['body'] = input("Новое тело заметки: ")
            list_of_dicts[id_note]['data_edit'] = datetime.datetime.now().strftime("%d %B %Y %H:%M:%S")
            print("\nРЕЗУЛЬТАТ РЕДАКТИРОВАНИЯ")
            for item in list_of_dicts[id_note]:
                print('{}: {}'.format(item, list_of_dicts[id_note][item]))
            save_db()
            print("\nЗаметка сохранена!")
            break
        elif action == 2:
            list_of_dicts.pop(id_note)
            save_db()
            print("\nЗаметка удалена!")
            break
        elif action == 3:
            break
        else:
            print("Неверный пункт меню. Повторите попытку.")


def find_notes():
    if len(list_of_dicts) == 0:
        print("Заметок нет")
        return
    else:
        print("\nПОИСК ЗАМЕТКИ")
        find = input("Введите для поиска: ")
        for i in range(len(list_of_dicts)):
            if find == list_of_dicts[i]['id'] or find in list_of_dicts[i]['head'] or find in list_of_dicts[i]['body']:
                return list_of_dicts[i]['id']


def view_note(id):
    for i in range(len(list_of_dicts)):
        if list_of_dicts[i]['id'] == id:
            id_note = i
            break
        if i + 1 == len(list_of_dicts):
            print("\nЗаметка не найдена!")
            return

    print()
    for item in list_of_dicts[id_note]:
        print('{}: {}'.format(item, list_of_dicts[id_note][item]))
    actions_notes(id_note)


print("Программа Заметки")
db = "notes_db.json"
list_of_dicts = open_db()
interface()
