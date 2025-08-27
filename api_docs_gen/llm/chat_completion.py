from ..common import http_request, configuration

def sendRequest(request: str, files: list[str], repoIndex: dict) -> dict:
    apiUrl = configuration.getConfigStringValue("llm_chat_completion_api_url")
    apiKey = configuration.getConfigStringValue("llm_chat_completion_api_key")
    llmModel = configuration.getConfigStringValue("llm_model")
    payload = {
        "model" : llmModel,
        "temperature": 0,
        "top_p": 1,
        "random_seed": 0,
        "messages": [
            { 
                "role": "system",  
                "content": "You are a precise, terse coding assistant. Return only the requested output in the format asked." 
            },
            { 
                "role": "user",    
                "content": request
            }
        ]
    }
    headers = {
        "Authorization": f"Bearer {apiKey}",
        "Content-Type": "application/json"
    }
    response = http_request.makeHttpRequest(apiUrl, "POST", headers, payload, 30000)
    return response