from httpx import AsyncClient


async def test_health(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_register_and_login(client: AsyncClient) -> None:
    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "eleve@example.tg",
            "full_name": "Ama Koffi",
            "password": "un-mot-de-passe-solide",
        },
    )
    assert register_response.status_code == 201

    login_response = await client.post(
        "/api/v1/auth/login",
        data={"username": "eleve@example.tg", "password": "un-mot-de-passe-solide"},
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
