import os
from PIL import Image
import numpy as np

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'BakingData.txt')

with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

for line in lines:
    def delete_specific_files(root_dir):
        target_files = ['CO.tga', 'MNRN.tga', 'C.tga', 'MOH.tga', 'N.tga', 'R.tga']
        for subdir, _, files in os.walk(root_dir):
            for file in files:
                if file in target_files:
                    file_path = os.path.join(subdir, file)
                    try:
                        os.remove(file_path)
                        print(f"Clean: {file_path}")
                    except Exception as e:
                        print(f"Can Not Clean: {file_path} Error: {e}")
    root_directory = line
    delete_specific_files(root_directory)