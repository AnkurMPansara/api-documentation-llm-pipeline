import json
from api_docs_gen.common import configuration
from api_docs_gen.crawler import load_repo, scan_repo
from api_docs_gen.llm import chat_completion

if __name__ == "__main__":
    gitRepo = input("Enter git repository from which to generate API docs: ")
    branch = input("Enter main git branch of the repository: ")
    repo = load_repo.loadRepo(gitRepo, branch)
    repoIndex = scan_repo.indexRepo(repo)
    apiResp = chat_completion.sendRequest("Generate a python code to print Hello World", [], {})
    print(json.dumps(apiResp))