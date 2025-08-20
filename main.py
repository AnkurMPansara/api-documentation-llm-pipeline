from api_docs_gen.common import configuration
from api_docs_gen.crawler import load_repo

if __name__ == "__main__":
    gitRepo = input("Enter git repository from which to generate API docs: ")
    branch = input("Enter main git branch of the repository: ")
    repo = load_repo.loadRepo(gitRepo, branch)