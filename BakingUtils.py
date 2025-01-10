import bpy
# Function
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