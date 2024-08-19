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
        ポストくん
        https://postcode.teraren.com/
    """
    
    # generate "result"data
    result: dict = {}

https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyC7dLXM_6HyFxVvLVPnCLnV2uTdwqgYOKM&language=ja&address=%E6%9D%B1%E4%BA%AC%E9%83%BD%E6%9D%BF%E6%A9%8B%E5%8C%BA%E8%B5%A4%E7%BE%BD
https://postcode.teraren.com/postcodes.json?s=%E6%9D%B1%E4%BA%AC%E9%83%BD%E5%8C%97%E5%8C%BA%E4%B8%8A%E5%8D%81%E6%9D%A1
    import unicodedata
    from typing import Pattern
    import re

if __name__=="__main__":
    import asyncio
    import aiohttp
