import os

from ..common import configuration

def crawlFiles(files: list[str]) -> dict[str, str]:
    result = {}
    for file in files:
        relativeFilePath = os.path.join("data/repositories/", file)
        absFilePath = configuration.getAbsolutePath(relativeFilePath)
        try:
            with open(absFilePath, "r", encoding="utf-8") as f:
                result[file] = f.read()
        except Exception:
            result[file] = ""
    return result