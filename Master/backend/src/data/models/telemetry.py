from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Telemetry(SQLModel, table=True):
    id          : Optional[int] = Field(primary_key=True, default=None)
    device_id   : str           = Field(foreign_key='device.id', ondelete='CASCADE', description='Device that sent this reading')
    timestamp   : datetime      = Field(index=True, description='Timestamp of the reading')
    sensor_type : str           = Field(index=True, description='Type of the sensor, e.g., temperature, humidity')
    value       : float         = Field(description='Sensor reading value')
