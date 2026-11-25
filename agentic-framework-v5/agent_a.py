import httpx
from fastapi import FastAPI, HTTPException
import asyncio
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

agent_b_url = os.getenv("AGENT_B_URL")
agent_c_url = os.getenv("AGENT_C_URL")

app = FastAPI()


class TaskRequest(BaseModel):
    x: float
    y: float
    op: str


@app.post("/analyze")
async def analyze(data: TaskRequest):

    async with httpx.AsyncClient(timeout=15.0) as client:

        # Step 1: Prepare Agent B's request data
        data_b = data.model_dump()

        response_b1 =client.post(
            agent_b_url,
            json=data_b
            )

        # Step 2: Prepare Agent C's request data
        data_c = data.model_dump()
        data_c.pop("op")
        response_c1 = client.post(
            agent_c_url,
            json=data_c
            )
                


        # Step 3: Call B and C concurrently
        # Hint: asyncio.gather(...)
        response_b, response_c = await asyncio.gather(
            response_b1,
            response_c1
        )

        # Step 4: Check both HTTP status codes
        response_b.raise_for_status()
        response_c.raise_for_status()
        # Step 5: Deserialize both responses
        return_b=response_b.json()
        return_c=response_c.json()

        # Step 6: Return the combined result
        return {
            "calculation":return_b, 
            "statistics": return_c
            }