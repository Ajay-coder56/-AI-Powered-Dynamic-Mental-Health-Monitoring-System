from fastapi import APIRouter

router = APIRouter()

# Check-in endpoints are served under /api/v1/users/{user_id}/check-ins
# This router is kept for backward compatibility with main.py imports.
# See app/routers/users.py for the active implementation.
