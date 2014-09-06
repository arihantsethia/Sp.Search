import os

rootDir = '/home/arihant/Github/Sp.Search/dataset/'

def mergeErrorFilesFolder(folderName, newFileName):
    newFile = open(rootDir+newFileName,'a')
    currDir = rootDir + str(folderName)
    dirList=os.listdir(currDir)
    dirList.sort()
    for fileName in dirList:
        filePath = os.path.join(currDir,fileName)
        fileContent = ""
        with open(filePath, 'r') as content_file:
            fileContent = content_file.read().strip()
        if(len(fileContent) > 0 && fileContent[-1]!= '\n'):
            fileContent+='\n'
        newFile.write(fileContent)
    newFile.close()
