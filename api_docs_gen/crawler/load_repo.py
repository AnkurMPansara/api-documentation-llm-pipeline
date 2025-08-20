import subprocess
import os
from ..common import configuration

def loadRepo(repo: str, branch: str) -> bool:
    result = True
    repoParentPath = configuration.getRepoFolder()
    repoName = os.path.splitext(os.path.basename(repo))[0]
    repoPath = os.path.join(repoParentPath, repoName)
    if doesRepoExist(repoParentPath, repo):
        result = updateRepo(repoPath)
    else:
        result = cloneRepo(repoParentPath, repo, branch)
    if not result:
        print("loadRepo failed")
    return result

def cloneRepo(repoParentPath: str, repo: str, defaultBranch: str) -> bool:
    if not os.path.exists(repoParentPath):
        os.makedirs(repoParentPath, exist_ok=True)
    try:
        subprocess.check_call(["git", "clone", "--branch", defaultBranch, repo], cwd=repoParentPath)
        print(f"Repository cloned into {repoParentPath} (branch: {defaultBranch})")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
        return False

def updateRepo(repoPath: str) -> bool:
    try:
        subprocess.check_call(["git", "pull"], cwd=repoPath)
        print(f"Repository updated")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error updating repository: {e}")
        return False

def doesRepoExist(repoParentPath: str, repo: str) -> bool:
    repoName = os.path.splitext(os.path.basename(repo))[0]
    repoPath = os.path.join(repoParentPath, repoName)
    return os.path.isdir(os.path.join(repoPath, ".git"))