import os
from PIL import Image
import numpy as np

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'BakingData.txt')
material_paths = []

with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

for line in lines:
    folder_path = line.strip()
    subfolders = []

    for folder_name in os.listdir(folder_path):
        if folder_name.startswith("Material") and os.path.isdir(os.path.join(folder_path, folder_name)):
            material_folder_path = os.path.join(folder_path, folder_name)
            material_paths.append(material_folder_path)

material_paths = [material.replace('\\', '/') for material in material_paths]

for material_path in material_paths:
    co_paths = []
    ca_paths = []
    mnrn_paths = []

    for folder_name in os.listdir(material_path):
        if os.path.isdir(os.path.join(material_path, folder_name)):
            co_paths.append(os.path.join(material_path, folder_name, 'CO.tga'))
            mnrn_paths.append(os.path.join(material_path, folder_name, 'MNRN.tga'))
            ca_paths.append(os.path.join(material_path, folder_name, 'CA.tga'))

    # 合并 C.tga 图像
    co_images = [np.array(Image.open(path)) for path in co_paths if os.path.exists(path)]
    if co_images:
        max_co_image_array = np.maximum.reduce(co_images)
        max_co_image = Image.fromarray(max_co_image_array)
        output_co_image_path = os.path.join(material_path, 'CO.tga')
        max_co_image.save(output_co_image_path)
        print(f"合并后的 CO.tga 保存到: {output_co_image_path}")

    # 合并 MNRN.tga 图像
    mnrn_images = [np.array(Image.open(path)) for path in mnrn_paths if os.path.exists(path)]
    if mnrn_images:
        max_mnrn_image_array = np.maximum.reduce(mnrn_images)
        max_mnrn_image = Image.fromarray(max_mnrn_image_array)
        output_mnrn_image_path = os.path.join(material_path, 'MNRN.tga')
        max_mnrn_image.save(output_mnrn_image_path)
        print(f"合并后的 MNRN.tga 保存到: {output_mnrn_image_path}")

    # 合并 CA.tga 图像
    ca_images = [np.array(Image.open(path)) for path in ca_paths if os.path.exists(path)]
    if ca_images:
        max_ca_image_array = np.maximum.reduce(ca_images)
        max_ca_image = Image.fromarray(max_ca_image_array)
        output_ca_image_path = os.path.join(material_path, 'CA.tga')
        max_ca_image.save(output_ca_image_path)
        print(f"合并后的 MNRN.tga 保存到: {output_ca_image_path}")