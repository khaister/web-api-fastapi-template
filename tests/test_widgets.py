async def test_health_needs_no_auth(client):
    resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


async def test_v1_requires_api_key(client):
    assert (await client.get("/api/v1/widgets")).status_code == 401
    assert (await client.get("/api/v1/widgets", headers={"X-API-Key": "wrong"})).status_code == 401


async def test_widget_crud(client, auth):
    payload = {"name": "sprocket", "description": "a small gear", "quantity": 3}

    created = await client.post("/api/v1/widgets", json=payload, headers=auth)
    assert created.status_code == 201
    widget = created.json()
    assert widget["name"] == "sprocket"
    assert widget["active"] is True

    listed = await client.get("/api/v1/widgets", headers=auth)
    assert [w["id"] for w in listed.json()] == [widget["id"]]

    patched = await client.patch(f"/api/v1/widgets/{widget['id']}", json={"quantity": 5}, headers=auth)
    assert patched.status_code == 200
    assert patched.json()["quantity"] == 5
    assert patched.json()["name"] == "sprocket"

    deleted = await client.delete(f"/api/v1/widgets/{widget['id']}", headers=auth)
    assert deleted.status_code == 204
    assert (await client.get(f"/api/v1/widgets/{widget['id']}", headers=auth)).status_code == 404


async def test_widget_validation(client, auth):
    resp = await client.post("/api/v1/widgets", json={"name": "bad", "description": "", "quantity": -1}, headers=auth)
    assert resp.status_code == 422
