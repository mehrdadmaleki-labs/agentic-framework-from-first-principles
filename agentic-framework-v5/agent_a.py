import httpx
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class TaskRequest(BaseModel):
    x: float
    y: float
    op: str


@app.post("/task")
async def execute_task(data: TaskRequest):

    agent_b_url = "http://127.0.0.1:8001/calculate"

    # Step 1: Create an asynchronous HTTP client
    async with httpx.AsyncClient() as client:
        # Step 2: Send data to Agent B using POST
        response = await client.post(
            agent_b_url, 
            json=data.model_dump()
            )
    
    # Step 3: Read Agent B's JSON response
    response.raise_for_status()
    result = response.json()

    # Step 4: Return that result to the external client
    return result