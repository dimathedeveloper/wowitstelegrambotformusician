import vk_api
import os


path, filename = os.path.split(os.path.abspath(__file__))


token = input("Введите токен:aaQ13axAPQEcczQa") # Запрашиваем токен

vk_session = vk_api.VkApi(token=token) # Авторизуемся
vk = vk_session.get_api()
photo = open(f'{path}/photo_pre.html', 'r', encoding="utf8")
file = photo.read()
file2 = photo.read()
file1 = photo.read()
photo.close()

try:
    getinfo = vk.account.getProfileInfo() # Получаем информацию о профиле
    iddd = getinfo["id"] # ID аккаунта
    vk_name = getinfo["first_name"] # Имя
    vk_rename = getinfo["last_name"] # Фамилию

    test = vk.messages.getConversations(count=200) # Получаем диалоги через токен
    num = test["count"] # Количество диалогов
    print(f"Всего найдено диалогов: {num}")
    print(f"Начинаю выгрузку фотографий | {vk_name} {vk_rename} - vk.com/id{iddd}")
    for i in test["items"]: # Идем по списку
        idd = i["conversation"]["peer"]["id"] # Вытаскиваем ID человека с  диалога
        peer_type = i['conversation']['peer']['type'] # Информация о диалоге (конференция это или человек)
        if peer_type == "user": # Ставим проверку конференции
            if idd > 0: # Ставим проверку на группы
                print(f"Выгрузка фотографий - {idd}")
                testtt = vk.users.get(user_ids=idd, fields="sex") # Получаем информацию о человеке
                for b in testtt: # Идем по списку
                    pol_ebaniy = b["sex"] # Вытаскиваем пол
                    if pol_ebaniy == 1: # Если девочка то:
                        fo = vk.messages.getHistoryAttachments(peer_id=idd, media_type='photo', start_from=0,
                                                                count=200,
                                                                preserve_order=1, max_forwards_level=45)
                        for i in fo["items"]: # Идем по списку вложений
                            for j in i["attachment"]["photo"]["sizes"]:
                                if j["height"] > 500 and j["height"] < 650: # Проверка размеров
                                    url = j["url"] # Получаем ссылку на изображение
                                    file += f'<img class="photos" src="{url}" alt="Не удалось загрузить (:" title="Найдено в диалоге - vk.com/id{idd}">' # Сохраняем в переменную
                    elif pol_ebaniy == 2: # Если мальчик то:
                        fo = vk.messages.getHistoryAttachments(peer_id=idd, media_type='photo', start_from=0,
                                                                count=200,
                                                                preserve_order=1, max_forwards_level=45)
                        for i in fo["items"]:
                            for j in i["attachment"]["photo"]["sizes"]:
                                if j["height"] > 500 and j["height"] < 650:
                                    url = j["url"]
                                    file1 += f'<img class="photos" src="{url}" alt="Не удалось загрузить (:" title="Найдено в диалоге - vk.com/id{idd}">'
                    else: # Иначе
                        fo = vk.messages.getHistoryAttachments(peer_id=idd, media_type='photo', start_from=0,
                                                                count=200,
                                                                preserve_order=1, max_forwards_level=45)
                        for i in fo["items"]:
                            for j in i["attachment"]["photo"]["sizes"]:
                                if j["height"] > 500 and j["height"] < 650:
                                    url = j["url"]
                                    file2 += f'<img class="photos" src="{url}" alt="Не удалось загрузить (:" title="Найдено в диалоге - vk.com/id{idd}">'
            else:
                print("Это группа!")
        else:
            print("Это конфа!")

        save_photo = open(f'{path}/Девочки - id{iddd}.html', 'w+', encoding="utf8") # Открываем файл
        save_photo.write(file) # Сохраняем диалог
        save_photo.close() # Закрываем
        save_photos = open(f'{path}/Мальчики - id{iddd}.html', 'w+', encoding="utf8")
        save_photos.write(file1)
        save_photos.close()
        save_photoss = open(f'{path}/Не определено - id{iddd}.html', 'w+', encoding="utf8")
        save_photoss.write(file2)
        save_photoss.close()


except Exception as e: # Исключения ошибок
    print(e)