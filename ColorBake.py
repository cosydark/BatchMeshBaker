import bpy
import csv

# Prepare
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
for image in bpy.data.images:
    bpy.data.images.remove(image)

# Set Fbx Path
fbx_file_path = 'C:/Users/cosyd/Desktop/Prefab_Item_Build_Yiji_Wall_4m5m/T_Item_Build_Yiji_Wall/MI_Item_Build_Yiji_Wall_Layout.fbx'
C_path = 'C:/Users/cosyd/Desktop/Prefab_Item_Build_Yiji_Wall_4m5m/T_Item_Build_Yiji_Wall/T_Item_Build_Yiji_Wall_C.tga'

# Import
bpy.ops.import_scene.fbx(filepath=fbx_file_path)

# Set Mesh Node Name
object_name = "SM_Item_Build_Yiji_Wall_4m5m_LOD0"

# Deselect All
bpy.ops.object.select_all(action='DESELECT')

# Select Mesh Node
bpy.data.objects[object_name].select_set(True)

# Set Mesh Node Active
bpy.context.view_layer.objects.active = bpy.data.objects[object_name]

obj = bpy.context.view_layer.objects.active

mat = None
# Get Mesh Node Material
if obj.data.materials:
    mat = obj.data.materials[0]
else:
    mat = bpy.data.materials.new(name="New_Material")
    obj.data.materials.append(mat)

# Use Material Node
mat.use_nodes = True
materialNodes = mat.node_tree.nodes

# Get Principled BSDF Node
principled_bsdf = materialNodes.get("Principled BSDF")
if not principled_bsdf:
    principled_bsdf = materialNodes.new(type='ShaderNodeBsdfPrincipled')

# Import Texture
tex_image_C = materialNodes.new('ShaderNodeTexImage')
tex_image_C.image = bpy.data.images.load(C_path)

# Link Texture
mat.node_tree.links.new(principled_bsdf.inputs['Base Color'], tex_image_C.outputs['Color'])

# Update View
bpy.context.view_layer.update()

# New Render Target
tex_image_bake = materialNodes.new('ShaderNodeTexImage')
bake_image = bpy.data.images.new(name='BakeImage', width=2048, height=2048, alpha=False)
bake_image.generated_color = (0, 0, 0, 1)  # Set Black
tex_image_bake.image = bake_image

# Add UV Map Node
uv_map_node_bake = materialNodes.new(type='ShaderNodeUVMap')
uv_map_node_bake.uv_map = "UV3"
uv_map_node_1 = materialNodes.new(type='ShaderNodeUVMap')
uv_map_node_1.uv_map = "uv"

# tex_image_bake Vector
mat.node_tree.links.new(tex_image_bake.inputs['Vector'], uv_map_node_bake.outputs['UV'])
mat.node_tree.links.new(tex_image_C.inputs['Vector'], uv_map_node_1.outputs['UV'])

tex_image_bake.select = True  # 选择 tex_image_bake 节点
materialNodes.active = tex_image_bake  # 设置活动节点