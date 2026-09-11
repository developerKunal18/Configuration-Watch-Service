import time
from threading import Lock
from flask import Flask,jsonify,request

app=Flask(__name__)
_lock=Lock()
_configs={}
_history={}

@app.get("/health")
def health(): return jsonify({"status":"ok"})

@app.put("/api/config/<service>")
def update(service):
    payload=request.get_json(silent=True) or {}
    config=payload.get("config")
    if not isinstance(config,dict): return jsonify({"error":"config_object_required"}),400
    with _lock:
        previous=_configs.get(service)
        version=previous["version"]+1 if previous else 1
        record={"version":version,"config":config,"updated_at":int(time.time())}
        _configs[service]=record
        _history.setdefault(service,[]).append(record.copy())
    return jsonify({"service":service,**record}),200 if previous else 201

@app.get("/api/config/<service>")
def get_config(service):
    with _lock:
        record=_configs.get(service)
        if not record: return jsonify({"error":"configuration_not_found","service":service}),404
        return jsonify({"service":service,**record})

@app.get("/api/config/<service>/changes")
def changes(service):
    try: since=int(request.args.get("since","0"))
    except ValueError: return jsonify({"error":"since_must_be_integer"}),400
    if since<0: return jsonify({"error":"since_must_be_non_negative"}),400
    with _lock: result=[r for r in _history.get(service,[]) if r["version"]>since]
    return jsonify({"service":service,"since":since,"changes":result,"count":len(result)})

@app.errorhandler(404)
def not_found(_): return jsonify({"error":"resource_not_found"}),404

if __name__=="__main__": app.run(host="0.0.0.0",port=5000,debug=True)
