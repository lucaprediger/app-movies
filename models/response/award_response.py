from pydantic import BaseModel


class ProducerIntervalResponse(BaseModel):
    producer: str
    interval: int
    previousWin: int
    followingWin: int

class AwardResponse(BaseModel):
    min: list[ProducerIntervalResponse]
    max: list[ProducerIntervalResponse]