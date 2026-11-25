from fastapi import FastAPI
from pydantic import BaseModel
from tools import operation

app = FastAPI()


class CalculationRequest(BaseModel):
    x: float
    y: float
    op: str


@app.post("/calculate")
async def calculate(data: CalculationRequest):

    result = operation(data.x, data.y, data.op)

    return {
        "status": "success",
        "message": result
    }