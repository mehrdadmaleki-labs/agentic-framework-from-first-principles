import asyncio
from fastapi import FastAPI
from tools import operation
from fastapi import HTTPException
from pydantic import BaseModel

app = FastAPI()

class CalculationRequestBody(BaseModel):
    x: float
    y: float
    op: str
    agent: str

@app.post("/calculate")
async def calculate(data: CalculationRequestBody):

    try:
        agent = data.agent

        if agent == "A1":
            await asyncio.sleep(5)
        elif agent == "A2":
            await asyncio.sleep(10)


        result = operation(data.x, data.y, data.op)

        return {
            "status": "success",
            "message": result
        }

    except (ValueError, TypeError, KeyError) as e:
        # Your task:
        # Raise HTTPException with status code 400
        raise HTTPException(
            status_code=400,
            detail= str(e)
        )
        