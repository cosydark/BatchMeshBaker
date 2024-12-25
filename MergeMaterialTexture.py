from PIL import Image
file_path = 'D:/BakingData_DefaultLit.txt'

# Read
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# For Each Line
for line in lines:
    line = line.strip()
    print(line)
    moh_image_path = line + '/MOH.tga'
    r_image_path = line + '/R.tga'
    c_image_path = line + '/C.tga'
    n_image_path = line + '/N.tga'
    mnrn_image_path = line + '/MNRN.tga'
    co_image_path = line + '/CO.tga'

    moh_image = Image.open(moh_image_path).convert('RGBA')
    c_image = Image.open(c_image_path).convert('RGBA')
    r_image = Image.open(r_image_path).convert('RGBA')
    n_image = Image.open(n_image_path).convert('RGBA')
    r_image_r = r_image.split()[0]
    moh_image_r, moh_image_g, moh_image_b, _ = moh_image.split()
    c_image_r, c_image_g, c_image_b, _ = c_image.split()
    n_image_r, n_image_g, n_image_b, _ = n_image.split()


    co_image = Image.merge('RGBA', (c_image_r, c_image_g, c_image_b, moh_image_g))
    mnrn_image = Image.merge('RGBA', (moh_image_r, n_image_g, r_image_r, n_image_r))
    co_image.save(co_image_path, format='TGA')
    mnrn_image.save(mnrn_image_path, format='TGA')