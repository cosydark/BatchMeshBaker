import os

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'BakingData.txt')
default_lit_shader_name = 'XRender/Environment/EV_DefaultLit'
default_lit_paths = []

# 读取文件
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 遍历每一行
for line in lines:
    folder_path = line.strip()
    subfolders = []

    # 遍历指定文件夹中的所有文件夹
    for folder_name in os.listdir(folder_path):
        if folder_name.startswith("Material") and os.path.isdir(os.path.join(folder_path, folder_name)):
            material_folder_path = os.path.join(folder_path, folder_name)
            for subfolder_name in os.listdir(material_folder_path):
                subfolder_path = os.path.join(material_folder_path, subfolder_name)
                if os.path.isdir(subfolder_path):
                    subfolders.append(subfolder_path.replace('\\', '/'))

    # 检查每个 subfolder_path 中的 ShaderData 文件
    for subfolder in subfolders:
        # 动态生成 ShaderData 文件名称
        shader_data_filename = subfolder + '/ShaderInfo.txt'
        shader_data_path = os.path.join(subfolder, shader_data_filename)
        if os.path.isfile(shader_data_path):
            with open(shader_data_path, 'r', encoding='utf-8') as shader_file:
                first_line = shader_file.readline().strip()
                if first_line == default_lit_shader_name:
                    default_lit_paths.append(subfolder)

# 将 valid_paths 写入 Defaultlit_paths.txt 文件
output_file_path = 'D:/BakingData_DefaultLit.txt'
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for path in default_lit_paths:
        output_file.write(path + '\n')