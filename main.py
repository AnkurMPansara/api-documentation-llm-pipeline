import json
import os

from api_docs_gen.common import configuration
from api_docs_gen.crawler import load_repo, scan_repo
from api_docs_gen.llm import chat_completion
from api_docs_gen.indexer import index_files

if __name__ == "__main__":
    gitRepo = input("Enter git repository from which to generate API docs: ")
    branch = input("Enter main git branch of the repository: ")
    repoPath = load_repo.loadRepo(gitRepo, branch)
    repoName = os.path.basename(repoPath)
    repoIndex = scan_repo.indexRepo(repoPath, repoName)
    index_files.enrichRepoIndex(repoIndex, repoName)
    scan_repo.saveIndex(repoIndex, repoName)
    print(json.dumps(chat_completion.sendRequest("Where is dev config values are stored in?", [], repoIndex, "")))