import os, chardet, urllib, string
import htmlparser, indexbuilder

rootDir = '/home/arihant/Github/Sp.Search/dataset/'
indexDir = rootDir + 'indices/'
errorLogFile = rootDir + 'errors/error.log'

parser = htmlparser.HtmlParser()

def iterateOverErrorFolder(errorFile, lineNumber):
    indexFileCount = 0
    filesIndexed = 0
    with open(errorFile,'r') as f:
        for line in f:
            if(lineNumber>=0):
                fileContent = ""
                with open(line, 'r') as content_file:
                    fileContent = content_file.read().strip()
                try:
                    print filePath
                    parser.parseHtml(fileContent)
                    wordList = parser.getTerms()
                    fileId = filePath.spilt('/')[-1]
                    indexBuilder.buildIndex(fileId, wordList)
                    if(filesIndexed>10**4):
                        indexBuilder.writeIndex(indexDir+('%03d' % indexFileCount))
                        indexBuilder.deleteIndex()
                        indexBuilder = indexbuilder.IndexBuilder()
                        filesIndexed = 0
                        indexFileCount += 1
                    filesIndexed +=1
                except:
                    errorLog.write(filePath+"\n")
            else:
                lineNumber -=1
            fileContent = ""
            
           
        
        errorLog.close()

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
        newFile.write(fileContent)
    newFile.close()
