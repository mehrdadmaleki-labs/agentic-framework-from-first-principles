from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class StatisticsRequest(BaseModel):
    x: float
    y: float


@app.post("/statistics")
async def statistics(data: StatisticsRequest):

    mean = (data.x + data.y) / 2

    return {
        "status": "success",
        "mean": mean
    }