import yaml
import os

def getConfigStringValue(key: str) -> str:
    filePath = getAbsolutePath("config/globalConfig.yaml")
    with open(filePath, "r") as cfg:
        data = yaml.safe_load(cfg)
    return str(data.get(key))

def getAbsolutePath(relativePath: str) -> str:
    baseDir = os.path.dirname(__file__)
    mainPath = os.path.abspath(os.path.join(baseDir, "../../"))
    return os.path.abspath(os.path.join(mainPath, relativePath))

def getRepoFolder() -> str:
    repoLocation = getConfigStringValue("repo_location")
    return getAbsolutePath(repoLocation)