from app import app


def get_client():
    app.config["TESTING"] = True
    return app.test_client()


def test_index():
    client = get_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.get_json()["service"] == "cloud-native-cicd-demo"


def test_health():
    client = get_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "healthy"


def test_ready():
    client = get_client()
    resp = client.get("/ready")
    assert resp.status_code == 200


def test_metrics():
    client = get_client()
    resp = client.get("/metrics")
    assert resp.status_code == 200
