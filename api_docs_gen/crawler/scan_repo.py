import os

def indexRepo(repoPath: str) -> dict:
    repoIndex = getFolderIndex(repoPath)
    return repoIndex
    

def getFolderIndex(folderPath: str) -> dict:
    folderIndex = {}
    for item in os.listdir(folderPath):
        itemPath = os.path.join(folderPath, item)
        if os.path.isdir(itemPath):
            folderIndex[item] = getFolderIndex(itemPath)
        else:
            folderIndex[item] = getFileIndex(itemPath)
    return folderIndex


def getFileIndex(filePath: str) -> dict:
    fileIndex = {}
    fileStats = os.stat(filePath)
    fileSize = fileStats.st_size
    fileType = os.path.splitext(filePath)[1]
    fileIndex["file_size"] = fileSize
    fileIndex["file_extension"] = fileType
    return fileIndex