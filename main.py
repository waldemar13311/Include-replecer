import glob

file_name = 'nginx.conf'
new_file_text = ""

# Читаем основной файл
with open(file_name) as file:
    # Построчно
    for line in file:
        # Если строка содержит include и не комментарий
        if line.__contains__("include") and (not line.strip().startswith('#')):
            # получаем маску файла справа от слова include
            included_mask_name = line.split()[1].replace(";", "")
            # в цикле проходимся по всем файлам,
            # которые соответствуют маске
            for included_file_name in glob.glob(included_mask_name):
                start_spaces_in_line = len(line) - len(line.lstrip())
                new_file_text += "\n"
                # добавляем в качестве комментария
                # имя файла над которым работали
                new_file_text += " " * start_spaces_in_line + "#include " + included_file_name + ";\n"
                with open(included_file_name) as included_file:
                    for line_in_included_file in included_file:
                        new_file_text += " " * start_spaces_in_line + line_in_included_file
                # после каждого прочитанного файла
                # добавляем новую строку
                new_file_text += "\n"
        else:
           new_file_text += line

print(new_file_text)