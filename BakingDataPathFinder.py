import os

def FindShaderPaths(FilePath, ShaderNames, OutputPaths):
    for ShaderName, OutputPath in zip(ShaderNames, OutputPaths):
        DefaultLitPaths = []

        # Read the file
        with open(FilePath, 'r', encoding='utf-8') as File:
            Lines = File.readlines()

        # Iterate through each line
        for Line in Lines:
            FolderPath = Line.strip()
            Subfolders = []

            # Iterate through all subfolders in the specified folder
            try:
                for FolderName in os.listdir(FolderPath):
                    if FolderName.startswith("Material") and os.path.isdir(os.path.join(FolderPath, FolderName)):
                        MaterialFolderPath = os.path.join(FolderPath, FolderName)
                        for SubfolderName in os.listdir(MaterialFolderPath):
                            SubfolderPath = os.path.join(MaterialFolderPath, SubfolderName)
                            if os.path.isdir(SubfolderPath):
                                Subfolders.append(SubfolderPath.replace('\\', '/'))

                # Check the ShaderData file in each subfolder
                for Subfolder in Subfolders:
                    # Dynamically generate the ShaderData file name
                    ShaderDataFilename = Subfolder + '/ShaderInfo.txt'
                    ShaderDataPath = os.path.join(Subfolder, ShaderDataFilename)
                    if os.path.isfile(ShaderDataPath):
                        with open(ShaderDataPath, 'r', encoding='utf-8') as ShaderFile:
                            FirstLine = ShaderFile.readline().strip()
                            if FirstLine == ShaderName:
                                DefaultLitPaths.append(Subfolder)
            except FileNotFoundError as E:
                print(f"File or folder not found: {E}")

        # Write valid paths to the output file
        with open(OutputPath, 'w', encoding='utf-8') as OutputFile:
            for Path in DefaultLitPaths:
                OutputFile.write(Path + '\n')

# Set file path and shader names
CurrentDir = os.path.dirname(os.path.abspath(__file__))
FilePath = os.path.join(CurrentDir, 'BakingData.txt')

ShaderNames = [
    'XRender/Environment/ThinWall',
    'XRender/Environment/EV_DefaultLit',
    'XRender/Environment/Trunk',
    'XRender/Environment/Fern',
    'XRender/Standard/Foliage',
    'XRender/Environment/EV_LayeredArchitecture',
    'XRender/Environment/EV_LayeredRock_New',
    'XRender/Environment/Bubble',
    'XRender/Environment/ICE_Parallax',
    'XRender/Environment/Vine',
    'XRender/Environment/EV_LayeredArchitecture',
]
OutputPaths = [
    'D:/BakingData_ThinWall.txt',
    'D:/BakingData_DefaultLit.txt',
    'D:/BakingData_Trunk.txt',
    'D:/BakingData_Fern.txt',
    'D:/BakingData_Foliage.txt',
    'D:/BakingData_LayeredArchitecture.txt',
    'D:/BakingData_LayeredRock.txt',
    'D:/BakingData_Bubble.txt',
    'D:/BakingData_ICE.txt',
    'D:/BakingData_Vine.txt',
    'D:/BakingData_LayeredArchitecture.txt',
]

# Call the function
FindShaderPaths(FilePath, ShaderNames, OutputPaths)