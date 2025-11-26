from datetime import datetime
from typing import Dict, Optional
from uuid import UUID, uuid4

from sqlalchemy import Column
from sqlmodel import SQLModel, Field, JSON, UniqueConstraint


class OutboxEvent(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint('device_id', 'event_type', 'is_processed', name='uq_device_event'),
    )

    id           : UUID               = Field(default_factory=uuid4, primary_key=True)
    device_id    : str                = Field(foreign_key='device.id', ondelete='CASCADE', index=True)
    event_type   : str                = Field(index=True)
    payload      : Dict[str, str]     = Field(default_factory=dict, sa_column=Column(JSON))
    created_at   : datetime           = Field(default_factory=datetime.now, index=True)
    processed_at : Optional[datetime] = Field(default=None, index=True)
    is_processed : bool               = Field(default=False, index=True)
