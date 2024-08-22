async def convert_postal_code_to_location(session, postal_code: str, **kwargs) -> dict[str, None | int | bool | str | list[dict[str, str | dict[str, str]]]]:
    """
    Converts a postal code to an address using a postal code API.
    Args:
        session: aiohttp.ClientSession()
        postal_code: The postal code to convert.
    Returns:
        A dictionary containing the location information or error information if an error occurs.
    API used:
        PostcodeJp
        https://console.postcode-jp.com/dashbord
    """
    from .check_of_postal_code import check_of_postal_code
    
    result: dict = {}
    
    # 郵便番号のフォーマットが正しいかを確認
    if check_of_postal_code(postal_code): # return:boolean
        import unicodedata
        from typing import Pattern
        import re
        import json
        
        # 全角の可能性もある為、半角に変換
        postal_code = unicodedata.normalize('NFKC', postal_code)
        
        pattern__hyphenated_postal_code: Pattern[str] = re.compile(r'([0-9]{3}-[0-9]{4})')
        pattern__non_hyphenated_postal_code: Pattern[str] = re.compile(r'([0-9]{7})')

        # ハイフンを取り除く
        if pattern__hyphenated_postal_code.search(postal_code):
            non_hyphenated_postal_code: str = pattern__hyphenated_postal_code.search(postal_code).group().replace('-','')
        elif pattern__non_hyphenated_postal_code.search(postal_code):
            non_hyphenated_postal_code: str = pattern__non_hyphenated_postal_code.search(postal_code).group()
        
        # URL
        base_url: str = "https://apis.postcode-jp.com/api/v6"
        url: str = f"{base_url}/postcodes/{non_hyphenated_postal_code}"
        # API_KEY
        API_KEY: str = kwargs.get('POSTCODE_JP_API_KEY', '')
        # headers
        headers: dict[str, str] = {"Content-Type": "application/json", "apikey": API_KEY}
        
        try:
            async with session.get(url = url, headers = headers) as response:
                response.raise_for_status()
                data: list = await response.json()

                # 該当する郵便番号が無い場合、空のデータが返却されるためデータが存在するかを確認
                if data:
                    result['status_code'] = response.status
                    result['is_success'] = True
                    result['results'] = []
                    
                    pattern__further_divisions: Pattern[str] = re.compile(r'([0-9０-９-－]+)$')
                    
                    for item in data:
                        result_object: dict = {}

                        # レスポンスデータをもとにクリーンデータへ整形
                        if "postcode" in item:
                            result_object['postal_code'] = item.get('postcode')
                        if "prefCode" in item:
                            result_object['prefecture_code'] = item.get('prefCode')
                        if "pref" in item:
                            result_object['ja'] = {}
                            result_object['ja']['prefecture'] = item.get('pref')
                        if "city" in item:
                            result_object['ja']['city'] = item.get('city')
                        if "town" in item:
                            # 町域に丁目、番地などが含まれていれば分割
                            if pattern__further_divisions.search(item.get('town')):
                                result_object['ja']['suburb'] = item.get('town').replace(pattern__further_divisions.search(item.get('town')).group(), '')
                                result_object['ja']['further_divisions'] = pattern__further_divisions.search(item.get('town')).group()
                            else:
                                result_object['ja']['suburb'] = item.get('town')
                        if "office" in item:
                            result_object['ja']['place'] = item.get('office')
                        if "allAddress" in item:
                            result_object['ja']['full_address'] = item.get('allAddress')
                        
                        if "fullWidthKana" in item:
                            result_object['kana'] = {}
                            if "pref" in item['fullWidthKana']:
                                result_object['kana']['prefecture'] = item['fullWidthKana'].get('pref')
                            if "city" in item['fullWidthKana']:
                                result_object['kana']['city'] = item['fullWidthKana'].get('city')
                            if "town" in item['fullWidthKana']:
                                # 町域に丁目、番地などが含まれていれば分割
                                if pattern__further_divisions.search(item['fullWidthKana'].get('town')):
                                    result_object['kana']['suburb'] = item['fullWidthKana'].get('town').replace(pattern__further_divisions.search(item['fullWidthKana'].get('town')).group(), '')
                                    result_object['kana']['further_divisions'] = pattern__further_divisions.search(item['fullWidthKana'].get('town')).group()
                                else:
                                    result_object['kana']['suburb'] = item['fullWidthKana'].get('town')
                            if "office" in item['fullWidthKana']:
                                result_object['kana']['place'] = item['fullWidthKana'].get('office')
                            if "allAddress" in item['fullWidthKana']:
                                result_object['kana']['full_address'] = item['fullWidthKana'].get('allAddress')
                        
                        if not "ja" in result_object:
                            result['results'].append(result_object)
                        elif not "further_divisions" in result_object['ja']:
                            result['results'].append(result_object)
                        elif not "location" in item:
                            result['results'].append(result_object)  
                        elif not "latitude" in item['location'] or not "longitude" in item['location']:
                            result['results'].append(result_object)
                        else:
                            result_object['location'] = {}
                            result_object['location']['lat'] = item['location'].get('latitude')
                            result_object['location']['lng'] = item['location'].get('longitude')
                            
                            result['results'].append(result_object)
                            
                        """
                        if "ja" in result_object:
                            if "further_divisions" in result_object['ja']:
                                if "location" in item:
                                    if "latitude" in item['location'] or "longitude" in item['location']:
                                        result_object['location'] = {}
                                        if "latitude" in item['location']:
                                            result_object['location']['lat'] = item['location'].get('latitude')
                                        if "longitude" in item['location']:
                                            result_object['location']['lng'] = item['location'].get('longitude')
                        
                        result['results'].append(result_object)
                        """
                
                else:
                    result['status_code'] = response.status
                    result['is_success'] = False
                    result['error'] = "Error: Matching value was not found"
                    
        # error handling
        except aiohttp.ClientError as err:
            result['status_code'] = response.status
            result['is_success'] = False
            result['error'] = f"API request error: {response.status} {err.message}"

        except Exception as err:
            result['status_code'] = response.status
            result['is_success'] = False
            result['error'] = "Unexpected error: An unexpected error has occurred"

    else:
        result['status_code'] = None
        result['is_success'] = False
        result['error'] = "Format error: Incorrectly formatted postal code"

    result_json = json.dumps(result, ensure_ascii=False, indent=4)
    return result_json

if __name__=="__main__":
    import asyncio
    import aiohttp
