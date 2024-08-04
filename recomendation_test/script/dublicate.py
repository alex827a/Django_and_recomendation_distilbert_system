def process_file(file_path, output_file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()  # Чтение содержимого файла

        # Разделение содержимого по ';', удаление пустых строк и пробельных символов
        items = [item.strip() for item in content.split(';') if item.strip()]

        # Преобразование списка в множество для удаления дубликатов
        unique_items = set(items)

        # Подсчет уникальных элементов
        print(f"Количество уникальных элементов: {len(unique_items)}")

        # Опционально: сохранение уникальных элементов обратно в файл
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write('; '.join(unique_items))  # Сохраняем с разделителем '; '

        print(f"Уникальные элементы сохранены в файл {output_file_path}")

    except FileNotFoundError:
        print("Файл не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Пути к файлам
file_path = 'product_name.txt'
output_file_path = 'product_name_output.txt'

# Вызов функции
process_file(file_path, output_file_path)
