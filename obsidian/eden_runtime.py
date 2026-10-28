"""EDEN local-first assistant runtime. No unrestricted command execution."""
import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass

@dataclass
class EdenResponse:
    text: str
    provider: str
    available: bool

class EdenRuntime:
    def __init__(self, endpoint=None, model=None):
        self.endpoint=(endpoint or os.environ.get("EDEN_OLLAMA_URL","http://127.0.0.1:11434")).rstrip("/")
        self.model=model or os.environ.get("EDEN_MODEL","qwen3:1.7b")
        if self.endpoint not in ("http://127.0.0.1:11434","http://localhost:11434"):
            raise ValueError("EDEN only accepts loopback Ollama endpoints")
    def chat(self, message, history=None):
        if not isinstance(message,str) or not message.strip():
            return EdenResponse("Enter a message.","validation",False)
        if len(message)>12000:
            return EdenResponse("Message exceeds local safety limit.","validation",False)
        history=history or []
        messages=[{"role":"system","content":"You are EDEN, the local-first OBSIDIAN OS assistant. Be accurate, privacy-conscious, and honest about tools. Never claim to have performed system actions. Security decisions must be approved and enforced by independent policy services."}]
        for item in history[-12:]:
            if isinstance(item,dict) and item.get("role") in ("user","assistant") and isinstance(item.get("content"),str):
                messages.append({"role":item["role"],"content":item["content"][:12000]})
        messages.append({"role":"user","content":message})
        body=json.dumps({"model":self.model,"messages":messages,"stream":False,"options":{"num_predict":512}}).encode()
        req=urllib.request.Request(self.endpoint+"/api/chat",data=body,headers={"Content-Type":"application/json"},method="POST")
        try:
            with urllib.request.urlopen(req,timeout=50) as resp:
                result=json.load(resp)
            content=result.get("message",{}).get("content","")
            if not isinstance(content,str) or not content.strip():
                raise ValueError("Local model returned an empty response")
            return EdenResponse(content,"ollama:"+self.model,True)
        except (urllib.error.URLError,TimeoutError,OSError,ValueError,KeyError) as exc:
            return EdenResponse("Local AI unavailable. Install Ollama, download a supported model and start its service. EDEN remains usable in offline help mode.","fallback",False)
