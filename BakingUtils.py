import bpy

def read_line(T, I):
    with open(T, 'r', encoding='utf-8') as File:
        Lines = File.readlines()
        if len(Lines) >= I + 1:
            return Lines[I].strip()
        else:
            return None

def CustomBake(TextureName, FolderPath, Node):
    bpy.ops.object.bake(type='EMIT')
    Node.image.filepath_raw = FolderPath + '/' + TextureName
    Node.image.file_format = 'TARGA'
    Node.image.save()

def GetMaterialNode(NodeName, Mat):
    N = None
    MaterialNodes = Mat.node_tree.nodes
    for node in MaterialNodes:
        if node.name == NodeName:
            N = node
            break
    return N

def SetNodeTexture(NodeName, ColorMode, FolderPath, Mat):
    Node = GetMaterialNode(NodeName, Mat)
    Node.image = bpy.data.images.load(FolderPath + NodeName + '.tga')
    Node.image.alpha_mode = "CHANNEL_PACKED";
    if ColorMode <= 0:
        Node.image.colorspace_settings.name = 'Non-Color'
    else:
        Node.image.colorspace_settings.name = 'sRGB'

def SetNodeFloat(NodeName, Value, Mat):
    Node = GetMaterialNode(NodeName, Mat)
    Node.outputs[0].default_value = Value

def SetNodeColor(NodeName, Value, Mat):
    Node = GetMaterialNode(NodeName, Mat)
    Node.inputs['Color'].default_value = Value

def ReadFloat(ShaderInfoPath, LineIndex):
    return float(read_line(ShaderInfoPath, LineIndex))

def ReadColor(ShaderInfoPath, LineIndex):
    ColorLine = read_line(ShaderInfoPath, LineIndex).split(',')
    return [float(ColorLine[0]), float(ColorLine[1]), float(ColorLine[2]), 1]

def ReadFloat2AsFloat(ShaderInfoPath, LineIndex, Index):
    Float2Line = read_line(ShaderInfoPath, LineIndex).split(',')
    return float(Float2Line[Index])

def BakeMaps(Mat, FolderPath, RenderTextureNode):
    # Color
    Mat.node_tree.links.new(GetMaterialNode('MInput', Mat).inputs['Surface'],GetMaterialNode('Out', Mat).outputs['CM_C'])
    GetMaterialNode('RenderTexture', Mat).image.colorspace_settings.name = 'sRGB'
    CustomBake('C.tga', FolderPath, RenderTextureNode)
    # Normal
    Mat.node_tree.links.new(GetMaterialNode('MInput', Mat).inputs['Surface'], GetMaterialNode('Out', Mat).outputs['CM_N'])
    RenderTextureNode.image.colorspace_settings.name = 'Non-Color'
    CustomBake('N.tga', FolderPath, RenderTextureNode)
    # MOH
    Mat.node_tree.links.new(GetMaterialNode('MInput', Mat).inputs['Surface'], GetMaterialNode('Out', Mat).outputs['CM_MOH'])
    RenderTextureNode.image.colorspace_settings.name = 'Non-Color'
    CustomBake('MOH.tga', FolderPath, RenderTextureNode)
    # Roughness
    Mat.node_tree.links.new(GetMaterialNode('MInput', Mat).inputs['Surface'], GetMaterialNode('Out', Mat).outputs['CM_R'])
    RenderTextureNode.image.colorspace_settings.name = 'Non-Color'
    CustomBake('R.tga', FolderPath, RenderTextureNode)
    # Alpha
    Mat.node_tree.links.new(GetMaterialNode('MInput', Mat).inputs['Surface'], GetMaterialNode('Out', Mat).outputs['CM_Alpha'])
    RenderTextureNode.image.colorspace_settings.name = 'Non-Color'
    CustomBake('Alpha.tga', FolderPath, RenderTextureNode)

def CleanProject(MaterialName):
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for Image in bpy.data.images:
        bpy.data.images.remove(Image)
    for Mesh in bpy.data.meshes:
        bpy.data.meshes.remove(Mesh)
    for Material in bpy.data.materials:
        if Material.name != MaterialName:
            bpy.data.materials.remove(Material)

def Init(FbxFilePath, MeshName, MaterialName):
    # Import
    bpy.ops.import_scene.fbx(filepath=FbxFilePath)
    # Select Mesh Node
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[MeshName].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[MeshName]
    # Select
    Obj = bpy.context.view_layer.objects.active
    Mat = bpy.data.materials.get(MaterialName)
    Mat = Mat.copy()
    Mat.name = MaterialName + ' Instance'
    # Set UV
    if Obj.data.uv_layers:
        for Layer in Obj.data.uv_layers:
            if Layer.name == "uv3":
                Obj.data.uv_layers.active = Layer
                break
    # Set Mesh Node Material
    if Obj and Mat:
        for i in range(len(Obj.data.materials)):
            Obj.data.materials[i] = Mat

def NewRenderTexture(Mat):
    # New RT
    RenderTexture = bpy.data.images.new(name='RenderTexture', width=2048, height=2048, alpha=False)
    RenderTexture.generated_color = (0, 0, 0, 1)
    RenderTextureNode = GetMaterialNode('RenderTexture', Mat)
    RenderTextureNode.image = RenderTexture
    RenderTextureNode.select = True
    Mat.node_tree.nodes.active = RenderTextureNode