import httpx
from fastapi import FastAPI, HTTPException
import asyncio
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

agent_b_url = os.getenv("AGENT_B_URL")

app = FastAPI()


class TaskRequest(BaseModel):
    x: float
    y: float
    op: str


@app.post("/task")
async def execute_task(data: TaskRequest):

    MAX_ATTEMPTS = 3

    try:
        async with httpx.AsyncClient(timeout=3.0) as client:

            for attempt in range(MAX_ATTEMPTS):

                try:
                    response = await client.post(
                        agent_b_url,
                        json=data.model_dump()
                    )

                    response.raise_for_status()
                    return response.json()

                except httpx.ConnectError:

                    # Step 1: Check whether this was the final attempt.

                    # Step 2: If final, raise HTTPException(503).
                    if attempt == MAX_ATTEMPTS - 1 :
                        raise HTTPException(503, "Agent B is not available")
                
                    delay = 2 ** attempt

                    print(f"Attempt {attempt + 1} failed. Retrying in {delay}s")
                    
                    await asyncio.sleep(delay)
            

                    # Step 3: Otherwise calculate the delay:
                    # delay = 2 ** attempt

                    # Step 4: Wait asynchronously:
                    # await asyncio.sleep(delay)
            

    except httpx.TimeoutException:
        # Challenge 2:
        # Raise HTTPException with status_code=504
        # detail="Agent B response timed out"
        raise HTTPException(
                    status_code=504,
                    detail="Agent B response timed out"
                )
        

    except httpx.HTTPStatusError as e:
        # Challenge 3:
        # Return an appropriate HTTP error
        # using e.response.status_code
        raise HTTPException(
                    status_code=e.response.status_code,
                    detail=e.response.text
                )