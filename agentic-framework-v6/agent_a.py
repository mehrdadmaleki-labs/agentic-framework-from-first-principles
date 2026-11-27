
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class TaskRequest(BaseModel):
    x: float
    y: float
    op: str


@app.post("/task")
async def execute_task(data: TaskRequest):

    async with httpx.AsyncClient() as client:

        # Step 1: Ask registry which agent supports data.op
        try:
            response = await client.get(
                f"http://127.0.0.1:8003/discover/{data.op}"
            )

            # Step 2: Check whether discovery succeeded
            response.raise_for_status()

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"No agent supports {data.op}"
            )

        # Step 3: Convert registry response to dictionary
        agent_info = response.json()

        # Step 4: Extract the agent's URL
        url = agent_info["url"]

        # Step 5: Send POST request to the discovered agent
        try:
            result_response = await client.post(
                url,
                json=data.model_dump()
            )

            result_response.raise_for_status()

            # Step 6: Return the agent's response
            return result_response.json()

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.text
            )
