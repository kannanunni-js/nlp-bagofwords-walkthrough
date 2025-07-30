from inference.io.api import api_router

@api_router.get(
    "/health",
    status_code=200,
    summary="Health Check API endpoint",
    description="Health Check API endpoint",
)
async def health():
    return {"message": "OK"}