import asyncio
import aiohttp
import uuid

API_URL = "https://localhost:7011/api/user/register"

TOTAL_REQUESTS = 1000
CONCURRENCY = 1000  # aynı anda kaç tane

sem = asyncio.Semaphore(CONCURRENCY)

async def send_request(session, index):
    async with sem:
        unique_id = uuid.uuid4().hex[:8]

        payload = {
            "Name":"DENEME",
            "Surname":"DENEME",
            "Username": f"user_{unique_id}",
            "Email": f"user_{unique_id}@test.com",
            "Password": "123456"
        }

        try:
            async with session.post(API_URL, json=payload, timeout=10) as resp:
                status = resp.status
                text = await resp.text()
                print(f"[{index}] Status: {status}")
        except Exception as e:
            print(f"[{index}] ERROR: {e}")

async def main():
    timeout = aiohttp.ClientTimeout(total=20)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [
            asyncio.create_task(send_request(session, i))
            for i in range(TOTAL_REQUESTS)
        ]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
