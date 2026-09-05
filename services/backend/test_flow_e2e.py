"""
Phase 2B End-to-End Development Flow Verification

Tests the complete victim data flow:
  user retrieval -> consent -> check-in assessment -> risk result -> history
"""
import asyncio
import httpx
import json

BASE = "http://localhost:8001"
PRIYA_ID = "11111111-1111-1111-1111-111111111111"

async def run_flow():
    async with httpx.AsyncClient() as c:
        print("=" * 60)
        print("PHASE 2B — END-TO-END DEVELOPMENT FLOW")
        print("=" * 60)

        # 1. Health
        r = await c.get(f"{BASE}/health")
        print(f"\n1. GET /health -> {r.status_code}: {r.json()}")
        assert r.status_code == 200

        # 2. Retrieve user
        r = await c.get(f"{BASE}/api/v1/users/{PRIYA_ID}")
        print(f"\n2. GET /api/v1/users/{PRIYA_ID}")
        print(f"   Status: {r.status_code}")
        data = r.json()
        print(f"   Name: {data['name']}")
        print(f"   Consent Given: {data['consent_given']}")
        assert r.status_code == 200

        # 3. Grant consent
        r = await c.post(
            f"{BASE}/api/v1/users/{PRIYA_ID}/consent",
            json={"consent_type": "data_collection_and_assessment"},
        )
        print(f"\n3. POST /api/v1/users/{PRIYA_ID}/consent")
        print(f"   Status: {r.status_code}")
        data = r.json()
        print(f"   Consent Given: {data['user_consent_given']}")
        print(f"   Consent Date: {data['user_consent_date']}")
        assert r.status_code == 201

        # 4. Submit check-in assessment
        payload = {
            "mode": "questionnaire",
            "mood": "anxious",
            "domain_scores": [
                {"domain": "mood", "score": 6},
                {"domain": "sleep", "score": 8},
                {"domain": "safety", "score": 3},
                {"domain": "social_support", "score": 5},
                {"domain": "legal_anxiety", "score": 7},
            ],
            "duration_seconds": 180,
        }
        r = await c.post(
            f"{BASE}/api/v1/users/{PRIYA_ID}/check-ins",
            json=payload,
        )
        print(f"\n4. POST /api/v1/users/{PRIYA_ID}/check-ins")
        print(f"   Status: {r.status_code}")
        data = r.json()
        print(f"   Check-in ID: {data['check_in_id']}")
        print(f"   Risk Score: {data['risk_score']}")
        print(f"   Risk Level: {data['risk_level']}")
        print(f"   Wellbeing Score: {data['wellbeing_score']}")
        print(f"   Contributing Factors: {data['contributing_factors']}")
        print(f"   Domain Scores: {json.dumps(data['domain_scores'])}")
        print(f"   Disclaimer: {data['disclaimer']}")
        assert r.status_code == 201

        # 5. Retrieve check-in history
        r = await c.get(f"{BASE}/api/v1/users/{PRIYA_ID}/check-ins")
        print(f"\n5. GET /api/v1/users/{PRIYA_ID}/check-ins")
        print(f"   Status: {r.status_code}")
        data = r.json()
        print(f"   Total check-ins: {len(data)}")
        if data:
            print(f"   Latest: id={data[0]['id']}, risk_level={data[0]['risk_level']}, created_at={data[0]['created_at']}")
        assert r.status_code == 200

        print("\n" + "=" * 60)
        print("ALL STEPS PASSED SUCCESSFULLY")
        print("=" * 60)

if __name__ == "__main__":
    asyncio.run(run_flow())
