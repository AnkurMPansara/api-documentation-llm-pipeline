import os
import json

from ..llm import chat_completion

def enrichRepoIndex(repoIndex: dict, repo: str):
    def generateFileContext(filePath: str, fileName: str) -> str:
        print(f"\nIndexing File {filePath}...")
        try:
            apiResp = chat_completion.sendRequest(f"Summarize file {fileName} in **one line only**, stating business requirement and tech stack, suitable for storing in repo index. Do **not** add explanations or file paths.", [filePath], repoIndex, "File implementing <brief functionality> using <tech stack/language>, serving as <role in repo> in repository, and used as part of <business purpose>.")
            if apiResp["status"] == "Success":
                llmResp = apiResp["response"]
                context = llmResp["choices"][0]["message"]["content"]
                print(f"Infurred context: {context}")
                return context
        except Exception:
            return ""
        return ""

    def lookupRepo(repoIndex: dict, parentDir: str):
        for name, value in repoIndex.items():
            currentPath = os.path.join(parentDir, name)
            if "file_extension" in value:
                if value.get("context", "") == "":
                    repoIndex[name]["context"] = generateFileContext(currentPath, name)
            else:
                lookupRepo(value, currentPath)
    
    lookupRepo(repoIndex, repo)

def getContextFromRepoIndex(repoIndex: dict) -> str:
    repoContext = []
    def traverseRepo(folder: dict, parentDir: str):
        for name, value in folder.items():
            if "context" in value:
                repoContext.append(f"\"{os.path.join(parentDir, name)}\": \"\"")
            else:
                traverseRepo(value, os.path.join(parentDir, name))
    traverseRepo(repoIndex, "")
    return json.dumps(repoContext)