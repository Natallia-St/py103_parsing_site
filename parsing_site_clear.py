import requests
import bs4
import csv
import json
from operator import itemgetter


# Создание функции
def parsing_av_site(link_):
    # Создание списков для каждого вида спаршенной информации
    url_list = []
    cost_rub_list = []
    cost_usd_list = []
    info_list = []
    # Скачиваем страницу по ссылке
    url_ = link_
    r = requests.get(url_)
    print(r.status_code)
    # Из скаченной HTML страницы делаем суп для дальнейшего получения нужной информации
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    # Получаем информацию с тегом и классом, в котором находится ссылка
    all_link = soup.find_all("h3", class_="listing-item__title")
    # Достаем текст из тэга, добавляем в соответствующий словарь для линки
    for link in all_link:
        url_cars = ("https://cars.av.by" + link.a["href"])
        url_list.append(url_cars)
        print(url_cars)
        # Скачиваем страницы по полученным ссылкам для каждой машины и делаем суп
        r_car = requests.get(url_cars)
        soup = bs4.BeautifulSoup(r_car.text, 'html.parser')
        # Получаем информацию с тегом и классом, в которм находится инфа о стоимости в руб.
        all_price_rub = soup.find_all("div", class_="card__price-primary")
        # Достаем цену из тэга, убираем лишние символы, кроме цифр, добавляем в свой список
        for all_price in all_price_rub:
            cost_rub = str(all_price.text)
            new_cost_rub = int(''.join([char for char in cost_rub if char.isdigit()]))
            print(new_cost_rub)
            cost_rub_list.append(new_cost_rub)
            # Получаем информацию с тегом и классом, в котором находится инфа о стоимости в долл.
            all_price_usd = soup.find_all("div", class_="card__price-secondary")
            # Достаем цену из тэга, убираем лишние символы, кроме цифр, добавляем в свой список
            for all_price in all_price_usd:
                cost_usd = str(all_price.text)
                new_cost_usd = int(''.join([char for char in cost_usd if char.isdigit()]))
                print(new_cost_usd)
                cost_usd_list.append((new_cost_usd))
                # Получаем информацию с тегом и классом, в которм находятся х-ки авто, добавляем в свой список.
                all_info_car = soup.find_all("div", class_="card__params")
                for all_info in all_info_car:
                    info = all_info.text
                    info1 = info.replace("\xa0", "")
                    info2 = info1.replace("\u2009", "")
                    print(info2)
                    info_list.append(info2)
    # Блок инструкций для объединения отдельных словарей с инфой в один, в котором эти словари будут вложенными
    total_info_spis = [[]]
    n = 0
    for i in url_list:
        if url_list.index(i) == n:
            total_info_spis.append([])
            total_info_spis[n].append(i)
            for j in cost_rub_list:
                if cost_rub_list.index(j) == n:
                    total_info_spis[n].append(j)
                    for t in cost_usd_list:
                        if cost_usd_list.index(t) == n:
                            total_info_spis[n].append(t)
                            for x in info_list:
                                if info_list.index(x) == n:
                                    total_info_spis[n].append(x)
        n += 1
    total_info_spis.pop(-1)  # Удаляю последний пустой вложенный словарь, не разобрадась  пока почему он добавляется
    # print("new", new)
    # Сортировка полученных вложенных списков по стоимости авто в долл
    total_info_spis_sort = sorted(total_info_spis, key=itemgetter(2))
    print("Список (отсортированный по цене в долл", total_info_spis_sort)
    # Содание из списка словаря, чтобы загрузить в json
    total_info_dict = {}
    for i in total_info_spis_sort:
        key = i[0]
        val = i[1:]
        total_info_dict[key] = val
    for key in total_info_dict:
        n = total_info_dict.get(key)

    # Добавила для стоимостей и х-ки ключи, чтобы удобно было смотреть json
    for key in total_info_dict:
        if total_info_dict[key][0]:
            key1 = "cost_rub"
            total_info_dict[key][0] = {key1: total_info_dict[key][0]}
        if total_info_dict[key][1]:
            key1 = "cost_usd"
            total_info_dict[key][1] = {key1: total_info_dict[key][1]}
        if total_info_dict[key][2]:
            key1 = "describe"
            total_info_dict[key][2] = {key1: total_info_dict[key][2]}
    print("Cловарь (отсортированный по цене в долл)", total_info_dict)
    # Выгрузка словаря в json
    data = total_info_dict
    with open("cars_info.json", "w", encoding='UTF-8') as file:
        json.dump(data, file)
    # Выгрузка списка в csv, для ясности добавлено наименование валюты для числа
    for i in total_info_spis_sort:
        i[1] = str(i[1]) + "," + "rub"
    for i in total_info_spis_sort:
        i[2] = str(i[2]) + "," + "usd"
    file_ = open('cars_info.csv', 'w', encoding='UTF-8', newline='')
    writer_ = csv.writer(file_, delimiter=';')
    data_ = total_info_spis_sort
    for row in data_:
        writer_.writerow(row)
    file_.close()


# Вызов функции
parsing_av_site("https://cars.av.by/bmw/m5")
