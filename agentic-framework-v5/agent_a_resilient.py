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


async def call_agent_with_retry(client, url, data):

    MAX_ATTEMPTS = 3

    for attempt in range(MAX_ATTEMPTS):

        try:
            response = await client.post(
                url,
                json=data
            )

            return response

        except httpx.ConnectError as e:

            # Step 1: If this is the last attempt,
            # return the exception object.
            if attempt == MAX_ATTEMPTS - 1:
                return e           

            # Step 2: Otherwise calculate the delay.
            delay = 2 ** attempt

            # Step 3: Wait without blocking the event loop.
            print(f"Attempt {attempt + 1} failed. Retrying in {delay}s")
                                
            await asyncio.sleep(delay)

@app.post("/analyze")
async def analyze(data: TaskRequest):

    async with httpx.AsyncClient(timeout=15.0) as client:

        # Step 1: Prepare Agent B's request data
        data_b = data.model_dump()

        # Step 2: Prepare Agent C's request data
        data_c = data.model_dump()
        data_c.pop("op")

        # Step 2: Call B and C concurrently
        response_b, response_c = await asyncio.gather(
            call_agent_with_retry(client, agent_b_url, data_b),
            call_agent_with_retry(client, agent_c_url, data_c),
            return_exceptions=True
        )

        def process_agent_response(response):

            # Connection or timeout error
            if isinstance(response, Exception):
                return {
                    "status": "error",
                    "type": type(response).__name__,
                    "message": str(response)
                }

            # HTTP error
            if response.is_error:
                return {
                    "status": "error",
                    "http_status": response.status_code,
                    "message": response.text
                }

            # Successful response
            return response.json()
            

        # Step 6: Return the combined result
        return {
            "calculation":process_agent_response(response_b), 
            "statistics": process_agent_response(response_c)
            }