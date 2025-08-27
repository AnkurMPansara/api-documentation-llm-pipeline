import json

from ..common import http_request, configuration
from ..crawler import crawl_file
from ..indexer import index_files

def sendRequest(request: str, files: list[str], repoIndex: dict, sampleResponse: str) -> dict:
    apiUrl = configuration.getConfigStringValue("llm_chat_completion_api_url")
    apiKey = configuration.getConfigStringValue("llm_chat_completion_api_key")
    llmModel = configuration.getConfigStringValue("llm_model")
    contextFiles = crawl_file.crawlFiles(files)
    messages = [
        { 
            "role": "system",  
            "content": "You are a precise, terse coding assistant. Return only the requested output in the format asked." 
        }
    ]
    if len(repoIndex) > 0:
        repoInstruction = {
            "role": "system",
            "content": f"You are given a repository index in JSON format. Each file entry may have a \"context\" key that contains a short summary of the file's purpose. Treat these summaries as authoritative.\nUse file and folder names as hints to infer the role of files in the repository:\n{index_files.getContextFromRepoIndex(repoIndex)}"
        }
        messages.append(repoInstruction)
    if len(contextFiles) > 0:
        for fileName, fileContent in contextFiles.items():
            if len(fileContent) > 0:
                fileIntruction = {
                    "role": "system",
                    "content": f"File {fileName}:\n{fileContent}"
                }
                messages.append(fileIntruction)
    if len(sampleResponse) > 0:
        sampleResponseInstruction = {
            "role": "system",
            "content": f"Use this format for the response:\n{sampleResponse}"
        }
        messages.append(sampleResponseInstruction)
    payload = {
        "model" : llmModel,
        "temperature": 0.5,
        "top_p": 0.5,
        #"random_seed": 0,
        "messages": messages
    }
    headers = {
        "Authorization": f"Bearer {apiKey}",
        "Content-Type": "application/json"
    }
    response = http_request.makeHttpRequest(apiUrl, "POST", headers, payload, 30000)
    return response