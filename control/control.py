import asyncio

async def control(requested_values: list[dict[str, str]], **kwargs) -> list[dict]:
    import aiohttp
    async with aiohttp.ClientSession() as session:
        tasks: list = []
        
        task1 = asyncio.create_task(coro_success())
        task2 = asyncio.create_task(coro_value_err())
        task3 = asyncio.create_task(coro_long(), name="残るコルーチン")  # 分かりやすくするためタスクに名づけ

        results = await asyncio.gather(*[task1, task2, task3])

        try:
            async with asyncio.TaskGroup() as g:
                task1 = g.create_task(coro_success())
                task2 = g.create_task(coro_value_err())
                task3 = g.create_task(coro_long(), name="残るコルーチン")
            results = [task1.result(), task2.result(), task3.result()]
            print(f"{results=}")
        except* ValueError as err:
            print(f"{err.exceptions=}")
    

        for requested_value in requested_values:
            if "postal_code" in requested_value:
                from .modules import convert_postal_code_to_location
                value: str = requested_value.get('postal_code')
                tasks.append(convert_postal_code_to_location(session, value, POSTCODE_JP_API_KEY = kwargs.get('POSTCODE_JP_API_KEY', '')))
                #await asyncio.sleep(2)
            """
            elif "address" in requested_value:
                value: str = requested_value.get('address')
                tasks.append(convert_location_to_postal_code(session, "address", value, GOOGLE_MAPS_API_KEY = kwargs.get('GOOGLE_MAPS_API_KEY', '')))
            
            elif "landmark" in requested_value:
                value: str = requested_value.get('landmark')
                tasks.append(convert_location_to_postal_code(session, "landmark", value, GOOGLE_MAPS_API_KEY = kwargs.get('GOOGLE_MAPS_API_KEY', '')))
            """
        results = await asyncio.gather(*tasks)
    
    return results
#asyncio.run(control([{ "postal_code" : "1008111" }], POSTCODE_JP_API_KEY = userdata.get('POSTCODE_JP_API_KEY')))
