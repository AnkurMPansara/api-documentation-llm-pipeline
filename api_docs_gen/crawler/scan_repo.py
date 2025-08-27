import os
import json

from ..common import configuration, writer

def indexRepo(repoPath: str, repoName: str) -> dict:
    repoIndex = loadIndex(repoName)
    if len(repoIndex) > 0:
        print("Just Loaded it")
        return repoIndex
    repoIndex = getFolderIndex(repoPath)
    return repoIndex
    

def getFolderIndex(folderPath: str) -> dict:
    folderIndex = {}
    for item in os.listdir(folderPath):
        itemPath = os.path.join(folderPath, item)
        if item in [".git", ".gitignore"]:
            continue
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

def saveIndex(repoIndex: str, repoName: str):
    saveLoc = configuration.getConfigStringValue("repo_index_location")
    filePath = configuration.getAbsolutePath(os.path.join(saveLoc, repoName+".json"))
    fileContent = json.dumps(repoIndex, indent=4)
    writer.writeInFile(filePath, fileContent)

def loadIndex(repoName: str) -> dict:
    saveLoc = configuration.getConfigStringValue("repo_index_location")
    filePath = configuration.getAbsolutePath(os.path.join(saveLoc, repoName+".json"))
    if not os.path.exists(filePath):
        return {}
    try:
        with open(filePath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}