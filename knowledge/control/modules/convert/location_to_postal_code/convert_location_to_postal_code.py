from typing import Any, Pattern, Literal
import re
import unicodedata

async def convert_location_to_postal_code(session, location_type: Literal["address", "landmark"], location: str, **kwargs) -> dict[str, None | int | bool | str | list[dict[str, str | dict[str, str]]]]:


if __name__=="__main__":
    import asyncio
    import aiohttp
