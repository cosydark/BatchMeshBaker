import bpy

file_path = 'E:/Git Project/BatchMeshBaker/BakingData.txt'

# Read
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# For Each Line
for line in lines:
    line = line.strip()
    # Set Fbx Path
    folder_path = line
    fbx_name = folder_path.split('/')[-1]
    fbx_file_path = folder_path + '/' + fbx_name + '.fbx'
    C_path = folder_path + '/' + fbx_name + '_C.tga'
    N_path = folder_path + '/' + fbx_name + '_N.tga'
    MOHR_path = folder_path + '/' + fbx_name + '_MOHR.tga'
    material_name = 'DefaultLit'
    object_name = fbx_name

    # Prepare
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for image in bpy.data.images:
        bpy.data.images.remove(image)
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)
    for material in bpy.data.materials:
        if material.name != material_name:
            bpy.data.materials.remove(material)

    # Import
    bpy.ops.import_scene.fbx(filepath = fbx_file_path)

    # Select Mesh Node
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[object_name].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[object_name]

    # Select
    obj = bpy.context.view_layer.objects.active
    mat = bpy.data.materials.get(material_name)
    mat = mat.copy()
    mat.name = material_name + ' Instance'

    # Get Mesh Node Material
    if obj and mat:
        for i in range(len(obj.data.materials)):
                obj.data.materials[i] = mat

    # Use Material Node
    mat.use_nodes = True
    materialNodes = mat.node_tree.nodes
    material_output = materialNodes.get("Material Output")
    material_output.location = (400, 0)

    # Import Texture
    tex_image_C = materialNodes.new('ShaderNodeTexImage')
    tex_image_C.image = bpy.data.images.load(C_path)
    tex_image_C.location = (-200, 0)

    tex_image_N = materialNodes.new('ShaderNodeTexImage')
    tex_image_N.image = bpy.data.images.load(N_path)
    tex_image_N.image.colorspace_settings.name = 'Non-Color'
    tex_image_N.location = (-200, 300)

    tex_image_MOHR = materialNodes.new('ShaderNodeTexImage')
    tex_image_MOHR.image = bpy.data.images.load(MOHR_path)
    tex_image_MOHR.image.colorspace_settings.name = 'Non-Color'
    tex_image_MOHR.location = (-200, 600)

    tex_image_M = materialNodes.new('ShaderNodeTexImage')
    mask_image = bpy.data.images.new(name='MaskImage', width=2048, height=2048, alpha=False)
    mask_image.generated_color = (1, 1, 1, 1)
    tex_image_M.image = mask_image
    tex_image_M.location = (-200, 900)

    # RT
    tex_image_bake = materialNodes.new('ShaderNodeTexImage')
    bake_image = bpy.data.images.new(name='BakeImage', width=2048, height=2048, alpha=False)
    bake_image.generated_color = (0, 0, 0, 1)
    tex_image_bake.image = bake_image
    tex_image_bake.location = (400, 300)

    # UV
    uv_map_node_bake = materialNodes.new(type='ShaderNodeUVMap')
    uv_map_node_bake.uv_map = "UV3"
    uv_map_node_bake.location = (200, 300)


    uv_map_node_1 = materialNodes.new(type='ShaderNodeUVMap')
    uv_map_node_1.uv_map = "uv"
    uv_map_node_1.location = (-500, 300)

    # Selection
    tex_image_bake.select = True
    materialNodes.active = tex_image_bake
    if obj.data.uv_layers:
        for uv_layer in obj.data.uv_layers:
            if uv_layer.name == "UV3":
                obj.data.uv_layers.active = uv_layer
                break

    # Link UV To TExture
    mat.node_tree.links.new(tex_image_bake.inputs['Vector'], uv_map_node_bake.outputs['UV'])
    mat.node_tree.links.new(tex_image_C.inputs['Vector'], uv_map_node_1.outputs['UV'])
    mat.node_tree.links.new(tex_image_N.inputs['Vector'], uv_map_node_1.outputs['UV'])
    mat.node_tree.links.new(tex_image_MOHR.inputs['Vector'], uv_map_node_1.outputs['UV'])

    # Bake And Place
    bpy.context.scene.cycles.bake_type = 'EMIT'

    def CustomBake(TextureName):
        bpy.ops.object.bake(type='EMIT')
        tex_image_bake.image.filepath_raw = folder_path + '/' + TextureName
        tex_image_bake.image.file_format = 'TARGA'
        tex_image_bake.image.save()


    # Bake Mask
    mat.node_tree.links.new(material_output.inputs['Surface'], tex_image_M.outputs['Color'])
    CustomBake('Mask.tga')
    # Color
    mat.node_tree.links.new(material_output.inputs['Surface'], tex_image_C.outputs['Color'])
    CustomBake('C.tga')
    # N
    mat.node_tree.links.new(material_output.inputs['Surface'], tex_image_N.outputs['Color'])
    CustomBake('N.tga')
    # MOH
    mat.node_tree.links.new(material_output.inputs['Surface'], tex_image_MOHR.outputs['Color'])
    CustomBake('MOH.tga')
    # R
    mat.node_tree.links.new(material_output.inputs['Surface'], tex_image_MOHR.outputs['Alpha'])
    CustomBake('R.tga')