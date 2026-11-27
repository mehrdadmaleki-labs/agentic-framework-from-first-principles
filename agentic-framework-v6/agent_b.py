from fastapi import FastAPI, HTTPException
from tools import operation
from pydantic import BaseModel

import httpx
from contextlib import asynccontextmanager


REGISTRY_URL = "http://127.0.0.1:8003/register"

@asynccontextmanager
async def lifespan(app: FastAPI):

    agent_info = {
        "name": "calculator",
        "url": "http://127.0.0.1:8001/calculate",
        "capabilities": [
            "ADD",
            "SUBTRACT",
            "MULTIPLY",
            "DIVISION"
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
        print("Agent B registered successfully")

    yield

    print("Agent B shutting down")


app = FastAPI(lifespan=lifespan)

class CalculationRequest(BaseModel):
    x: float
    y: float
    op: str


@app.post("/calculate")
async def calculate(data: CalculationRequest):
    try:
        result = operation(data.x, data.y, data.op)
        return {"status": "success", "message": result}

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
        
    
