import http.client
import json
from urllib.parse import urlparse

def makeHttpRequest(apiUrl: str, method: str, headers: dict = {}, payload: dict = {}, timeout: int = 3000) -> dict:
    headers = headers or {}
    parsedUrl = urlparse(apiUrl)

    if parsedUrl.scheme == "https":
        conn = http.client.HTTPSConnection(parsedUrl.netloc, timeout=timeout)
    else:
        conn = http.client.HTTPConnection(parsedUrl.netloc, timeout=timeout)

    requestBody = json.dumps(payload) if payload else None
    if requestBody:
        headers.setdefault("Content-Type", "application/json")
    
    try:
        conn.request(method.upper(), parsedUrl.path, requestBody, headers)
        resp = conn.getresponse()
        respData = resp.read().decode()
        
        try:
            apiResponse = json.loads(respData)
        except json.JSONDecodeError:
            pass
        return {
            "code" : resp.status,
            "status" : "Success",
            "response" : apiResponse
        }
    except Exception as e:
        code = getattr(resp, "status", None)
        return {
            "code" : code,
            "status" : "Failure",
            "response" : None
        }
    finally:
        try:
            if conn:
                conn.close()
        except Exception:
            # best-effort close; swallow exceptions
            pass