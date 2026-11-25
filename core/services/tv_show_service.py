from core.clients.sample_api.futurama_client import FuturamaClient
from core.dtos.tv_show_dtos import Person, TvShow, TvShows


def _parse_years(years_aired: str | None) -> tuple[int | None, int | None]:
    """Turn a range such as "1999–2013" into (start, stop); a missing end year means still airing."""
    if not years_aired:
        return None, None
    start, _, stop = years_aired.partition("–")
    return (int(start) if start.strip().isdigit() else None, int(stop) if stop.strip().isdigit() else None)


async def get_shows() -> TvShows:
    shows = []
    futurama = await FuturamaClient().get_show_info()
    if futurama:
        year_start, year_stop = _parse_years(futurama.years_aired)
        shows.append(
            TvShow(
                id=futurama.id,
                synopsis=futurama.synopsis,
                year_start=year_start,
                year_stop=year_stop,
                creators=[Person(name=creator.name, url=creator.url) for creator in futurama.creators],
            )
        )

    return TvShows(shows=shows)
