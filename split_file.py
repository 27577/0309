import os

def split_file(original_file, line_count=50):
    with open(original_file, 'r', encoding='utf-8') as file:
        file_lines = file.readlines()

    # 使用original_file的基础名称（不含扩展名）作为目录名的一部分
    base_name = os.path.splitext(os.path.basename(original_file))[0]
    output_folder = f'{base_name}_split'
    
    # 确保文件夹存在，用于存放分割后的文件
    os.makedirs(output_folder, exist_ok=True)

    file_index = 1
    for i in range(0, len(file_lines), line_count):
        part_file_path = os.path.join(output_folder, f'{file_index}.tbl')
        with open(part_file_path, 'w', encoding='utf-8') as file:
            file.writelines(file_lines[i:i+line_count])
        file_index += 1

    return file_index - 1  # 返回创建的文件数


