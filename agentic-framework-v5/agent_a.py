import httpx
from fastapi import FastAPI, HTTPException
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

    try:
        async with httpx.AsyncClient(timeout=3.0) as client:

            response = await client.post(
                agent_b_url,
                json=data.model_dump()
            )

            response.raise_for_status()

            return response.json()

    except httpx.ConnectError:
        # Challenge 1:
        # Raise HTTPException with status_code=503
        # detail="Agent B is unavailable"
        raise HTTPException(
            status_code=503,
            detail="Agent B is unavailable"
        )
        

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