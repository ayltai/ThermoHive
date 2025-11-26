from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Device(SQLModel, table=True):
    id           : str           = Field(primary_key=True, description='Unique identifier for the device')
    display_name : Optional[str] = Field(default=None, description='Human-readable name of the device')
    mode         : Optional[str] = Field(default=None, description='Operating mode of the device')
    last_seen    : datetime      = Field(index=True, description='Last time the device was seen online')
