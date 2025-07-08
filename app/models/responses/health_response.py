from datetime import datetime
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str = "Healthy"
    timestamp: str = str(datetime.now())
