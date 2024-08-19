#from typing import Literal

async def convert_location_to_postal_code(session, location_type: Literal["address", "landmark"], location: str, **kwargs) -> dict[str, None | int | bool | str | list[dict[str, str | dict[str, str]]]]:
    """
    Converts a location to an postal code using a geo API.
    Args:
        session: aiohttp.ClientSession()
        location_type: Location type
        location: The location to convert.
    Returns:
        A dictionary containing the postal code information or error information if an error occurs.
    API used:
        Google maps Platform
        https://console.cloud.google.com/google/maps-apis/api-list?project=api-project-430803&authuser=2&hl=ja
    """


    
    import unicodedata
    from typing import Pattern
    import re

if __name__=="__main__":
    import asyncio
    import aiohttp
