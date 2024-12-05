import glob

def replace_include_in_file(file_name, offset=0):
    new_file_text = ""

    try:
        with open(file_name) as file:
            for line in file:
                start_spaces_in_line = len(line) - len(line.lstrip())

                # Если строка содержит include и не комментарий
                if "include" in line and not line.strip().startswith('#'):

                    # Получаем маску файла справа от слова include
                    included_mask_name = line.split()[1].replace(";", "")
                    included_files = glob.glob(included_mask_name)

                    if not included_files:
                        # Если файлы по маске не найдены, добавляем сообщение
                        new_file_text += " " * (offset + start_spaces_in_line) + f"#include {included_mask_name} - file not found\n"
                    else:
                        # В цикле проходимся по всем файлам, которые соответствуют маске
                        for included_file_name in included_files:
                            # Добавляем в качестве комментария имя файла, которое подставили вместо include
                            new_file_text += "\n"
                            new_file_text += " " * (offset + start_spaces_in_line) + f"#include {included_file_name};\n"

                            # Рекурсивно обрабатываем включенный файл
                            new_file_text += replace_include_in_file(included_file_name, offset + start_spaces_in_line)
                else:
                    # Если строка не содержит include, просто добавляем её
                    new_file_text += " " * offset + line

    except FileNotFoundError:
        # Если текущий файл не найден, добавляем сообщение
        new_file_text += " " * offset + f"#include {file_name} - file not found\n"

    # После каждого прочитанного файла добавляем новую строку
    return new_file_text + "\n"


# Основной файл для обработки
nginx_main_file = 'nginx.conf'

# Обрабатываем файл и выводим результат
final_text = replace_include_in_file(nginx_main_file)
print(final_text)