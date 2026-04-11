from fastapi import FastAPI
from middleware.rate_limit import RateLimitMiddleware
from routes.parser import router as parser_router

app = FastAPI()
app.add_middleware(RateLimitMiddleware, uuid_limit=1, ip_limit=10, window=60)
app.include_router(parser_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
