import json

def update_product_names(json_file_path, txt_file_path, output_json_file_path):
    # Чтение списка названий товаров из текстового файла
    with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
        # Считываем весь файл, удаляем пробелы и разбиваем по запятой
        product_names = txt_file.read().strip().split(';')

    # Чтение и изменение JSON файла
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        
        # Предполагаем, что data - это список словарей
        for i, entry in enumerate(data):
            if i < len(product_names):
                entry['product_name'] = product_names[i].strip()  # Обновляем название продукта
            else:
                break  # Если товаров больше, чем названий, прерываем цикл

    # Сохранение изменений в новый JSON файл с указанием кодировки UTF-8
    with open(output_json_file_path, 'w', encoding='utf-8') as json_output_file:
        json.dump(data, json_output_file, ensure_ascii=False, indent=4)  # Форматированный вывод для лучшей читаемости

# Пути к файлам
json_file_path = 'all_products_ratings.json'
txt_file_path = 'product_name_output.txt'
output_json_file_path = 'updated_jsonfile.json'

# Вызов функции для обновления названий товаров
update_product_names(json_file_path, txt_file_path, output_json_file_path)
