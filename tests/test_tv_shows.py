from core.clients.sample_api.futurama_client import FuturamaClient
from core.clients.sample_api.futurama_dtos import Creator, Info
from core.services.tv_show_service import _parse_years


def test_parse_years():
    assert _parse_years("1999–2013") == (1999, 2013)
    assert _parse_years("2023–") == (2023, None)
    assert _parse_years(None) == (None, None)


async def test_list_tv_shows(client, auth, monkeypatch):
    async def fake_get_show_info(self):
        return Info(
            id=1,
            synopsis="A pizza delivery boy wakes up in the future.",
            yearsAired="1999–2013",
            creators=[Creator(name="Matt Groening", url="https://example.com/matt")],
        )

    monkeypatch.setattr(FuturamaClient, "get_show_info", fake_get_show_info)

    resp = await client.get("/api/v1/tv-shows", headers=auth)

    assert resp.status_code == 200
    show = resp.json()["shows"][0]
    assert show["year_start"] == 1999
    assert show["year_stop"] == 2013
    assert show["creators"] == [{"name": "Matt Groening", "url": "https://example.com/matt"}]
