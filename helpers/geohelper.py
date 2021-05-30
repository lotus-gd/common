import aiohttp

async def get_country(ip: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://ip.zxq.co/{ip}") as resp:
            json = await resp.json()
            return json["country"].upper()