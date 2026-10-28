"""Defensive local security events and deterministic triage."""
import json
import os
import pathlib
import stat
from datetime import datetime,timezone
from eden import evaluate_event

def check_path(path):
    p=pathlib.Path(path).expanduser()
    try:
        meta=p.stat()
        world_writable=bool(meta.st_mode & stat.S_IWOTH)
        severity=8 if world_writable else 1
        decision=evaluate_event("file_permissions",True,severity)
        return {"path":str(p),"exists":True,"world_writable":world_writable,"severity":severity,"decision":decision.action,"reason":decision.reason}
    except OSError as e:
        return {"path":str(p),"exists":False,"severity":0,"decision":"REVIEW","reason":"Unable to inspect path: "+str(e)}

def event_record(category,description,authorized,severity):
    decision=evaluate_event(category,authorized,severity)
    return {"timestamp":datetime.now(timezone.utc).isoformat(),"category":category,"description":description,"severity":severity,"decision":decision.action,"reason":decision.reason}

def append_audit(path,record):
    p=pathlib.Path(path).expanduser()
    p.parent.mkdir(parents=True,exist_ok=True)
    fd=os.open(str(p),os.O_WRONLY|os.O_CREAT|os.O_APPEND,0o600)
    with os.fdopen(fd,"a",encoding="utf-8") as f:
        f.write(json.dumps(record,ensure_ascii=False)+"\n")
