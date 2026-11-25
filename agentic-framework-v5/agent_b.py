from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tools import operation

app = FastAPI()


class CalculationRequest(BaseModel):
    x: float
    y: float
    op: str


@app.post("/calculate")
async def calculate(data: CalculationRequest):

    try: 

        result = operation(data.x, data.y, data.op)

        return {
            "status": "success",
            "message": result
        }
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )