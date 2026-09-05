import asyncio
import httpx

async def test_live_endpoints():
    async with httpx.AsyncClient() as client:
        # 1. Health
        try:
            r1 = await client.get("http://localhost:8000/health")
            print(f"Health: {r1.status_code} - {r1.text}")
            
            # 2. Login
            r2 = await client.post("http://localhost:8000/api/v1/auth/login", data={"username": "dr.meera.iyer@wcd.gov.in", "password": "password123"})
            print(f"Login: {r2.status_code}")
            
            if r2.status_code == 200:
                token = r2.json()["access_token"]
                
                # 3. Auth Me
                r3 = await client.get("http://localhost:8000/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
                print(f"Auth Me: {r3.status_code}")
                print(f"Auth Me Name: {r3.json().get('name')}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_live_endpoints())
