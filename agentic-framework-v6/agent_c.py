from fastapi import FastAPI, HTTPException
from tools import operation
from pydantic import BaseModel

import httpx
from contextlib import asynccontextmanager


REGISTRY_URL = "http://127.0.0.1:8003/register"

@asynccontextmanager
async def lifespan(app: FastAPI):

    agent_info = {
        "name": "statistics",
        "url": "http://127.0.0.1:8002/statistics",
        "capabilities": [
            "MEAN",
            "MAX"
        ]
    }

    async with httpx.AsyncClient() as client:

        # Step 1: Send POST request to registry
        response = await client.post(
            REGISTRY_URL,
            json=agent_info
        )

        # Step 2: Check registration succeeded
        response.raise_for_status()

        # Step 3: Print confirmation
        print("Agent C registered successfully")

    yield

    print("Agent C shutting down")


app = FastAPI(lifespan=lifespan)


class StatisticsRequest(BaseModel):
    x: float
    y: float
    op: str

@app.post("/statistics")
async def statistics(data: StatisticsRequest):
    if data.op == "MEAN":
        mean = (data.x + data.y) / 2
        return {"mean": mean}
    elif data.op == "MAX":
        if data.x < data.y:
            return {"max":data.y}
        else:
            return {"max":data.x}

    raise HTTPException(
        status_code=400,
        detail=f"Operation {data.op} is not supported"
        )
