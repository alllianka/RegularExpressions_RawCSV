from logging import lastResort
from pprint import pprint
import csv
import re
# читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
# pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ
'''
1. Поместить Фамилию, Имя и Отчество человека в поля lastname, firstname и surname соответственно. 
Ф+И+О. Подсказка: работайте со срезом списка (три первых элемента) при помощи " ".join([:2]) и split(" "), регулярки здесь НЕ НУЖНЫ.
2. Привести все телефоны в формат +7(999)999-99-99. Если есть добавочный номер, формат будет такой: +7(999)999-99-99 доб.9999.
Подсказка: используйте регулярки для обработки телефонов.
3. Объединить все дублирующиеся записи о человеке в одну. Подсказка: группируйте записи по ФИО (если будет сложно, допускается группировать только по ФИ).
'''
# ваш код
clear_contact_list = []
# обработка номера телефона
for contact in contacts_list:
    phone_number = contact[5]
    phone_pattern = r"(?:\+7|8)\D*(\d{3})\D*(\d{3})\D*(\d{2})\D*(\d{2})(?:\D*доб\.?\D*(\d+))?"
    # функция для преобразования номеров в единый формат
    def format_match(match):
        code, num1, num2, num3, ext = match.groups()
        result = f"+7({code}){num1}-{num2}-{num3}"
        if ext:
            result += f" доб.{ext}"
        return result
    cleaned_phones = re.sub(phone_pattern, format_match, phone_number)

for row in contacts_list:
    lastnames = row[0].split(' ')
    firstnames = row[1].split(' ')
    surnames = row[2].split(' ')
    organization = row[3].split(' ')
    position = [row[4]]
    phone = [row[5]]
    email = [row[6]]
    lfs = (lastnames + firstnames + surnames)[:3] + organization + position + phone + email# Фамилия, имя, отчество
    if lfs not in clear_contact_list:
        clear_contact_list.append(lfs)
#pprint(clear_contact_list)

# Объединяем повторяющиеся контакты в одну строку
merged_dict = {}
for contact in clear_contact_list:
    # Предположим, что ФИО находится в первых трех полях
    key = (contact[0], contact[1])  # Фамилия, Имя как ключ

    if key not in merged_dict:
        merged_dict[key] = contact.copy()
    else:
        # Объединяем информацию, заполняя пустые поля
        for i in range(len(contact)):
            if not merged_dict[key][i] and contact[i]:
                merged_dict[key][i] = contact[i]

# Делаем список из значений словаря
clear_contact_list = list(merged_dict.values())



if __name__ == '__main__':
    # # TODO 2: сохраните получившиеся данные в другой файл
    with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
        datawriter = csv.writer(f, delimiter=',')
        # Вместо contacts_list подставьте свой список
        datawriter.writerows(clear_contact_list)
    print("Преобразование содержания csv таблицы выполнено")

