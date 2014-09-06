import os, chardet, urllib, string
import htmlparser, indexbuilder

rootDir = '/home/arihant/Github/Sp.Search/dataset/'
indexDir = rootDir + 'indices/'
errorLogFile = rootDir + 'error.log'

parser = htmlparser.HtmlParser()

def iterateOverFolders(startFolder, endFolder):
    for folderNumber in xrange(startFolder,endFolder):
        indexBuilder = indexbuilder.IndexBuilder()
        errorLog = open(errorLogFile+str(folderNumber), 'w')
        currDir = rootDir + str(folderNumber)
        dirList=os.listdir(currDir)
        dirList.sort()
        for fileName in dirList:
            filePath = os.path.join(currDir,fileName)
            fileContent = ""
            with open(filePath, 'r') as content_file:
                fileContent = content_file.read().strip()
            try:
                print filePath
                parser.parseHtml(fileContent)
                wordList = parser.getTerms()
                indexBuilder.buildIndex(int(fileName), wordList)
            except:
                errorLog.write(filePath+"\n")
        indexBuilder.writeIndex(indexDir+('%03d' % folderNumber))
        indexBuilder.deleteIndex()
        errorLog.close()

startFolder = int(input("Enter start folder : "))
endFolder = int(input("Enter end folder : "))

iterateOverFolders(startFolder, endFolder)