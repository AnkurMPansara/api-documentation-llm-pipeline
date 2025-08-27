import os

def writeInFile(filePath: str, fileContent: str):
    parentDir = os.path.dirname(filePath)
    if parentDir:
        os.makedirs(parentDir, exist_ok=True)
    with open(filePath, "w", encoding="utf-8") as f:
        f.write(fileContent)