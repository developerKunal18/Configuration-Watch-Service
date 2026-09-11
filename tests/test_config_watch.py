import app as m

def setup_function():
    m._configs.clear();m._history.clear()

def test_health():
    assert m.app.test_client().get("/health").status_code==200

def test_create():
    r=m.app.test_client().put("/api/config/payment",json={"config":{"timeout":30}})
    assert r.status_code==201 and r.json["version"]==1

def test_versioning():
    c=m.app.test_client()
    c.put("/api/config/payment",json={"config":{"timeout":10}})
    r=c.put("/api/config/payment",json={"config":{"timeout":20}})
    assert r.status_code==200 and r.json["version"]==2

def test_changes_since():
    c=m.app.test_client()
    for n in (10,20,30): c.put("/api/config/payment",json={"config":{"timeout":n}})
    r=c.get("/api/config/payment/changes?since=1")
    assert r.json["count"]==2
    assert [x["version"] for x in r.json["changes"]]==[2,3]

def test_latest_has_no_changes():
    c=m.app.test_client()
    c.put("/api/config/payment",json={"config":{"timeout":30}})
    assert c.get("/api/config/payment/changes?since=1").json["count"]==0

def test_invalid_since():
    assert m.app.test_client().get("/api/config/payment/changes?since=x").status_code==400

def test_missing_config():
    assert m.app.test_client().put("/api/config/payment",json={"config":"bad"}).status_code==400

def test_get():
    c=m.app.test_client()
    c.put("/api/config/payment",json={"config":{"retries":3}})
    r=c.get("/api/config/payment")
    assert r.status_code==200 and r.json["config"]["retries"]==3
